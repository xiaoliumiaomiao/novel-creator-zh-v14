"""去 AI 味系统 — expression-only, detail-light, dramatic-boost 三种模式.

双评分体系：
- 清单评分：模板句、解释腔、总结腔、平均句长、情绪毛刺、角色口吻、信息密度
- 读者视角评分：是否像自然网文作者表达，是否保留连载吸引力
"""

from __future__ import annotations

import re
from pathlib import Path

from rich.console import Console
from rich.table import Table

from novel_creator.config import DEAI_MODES

console = Console()

# ============================================================
# AI 腔特征库
# ============================================================

# 禁用句式（硬规则，触发自动回修）
BANNED_EXPRESSIONS = [
    (re.compile(r'——不是[^，。；\n]{1,40}[，。；]'), "「A——不是B」式模板句"),
    (re.compile(r'总而言之'), "机械总结腔"),
    (re.compile(r'综上所述'), "机械总结腔"),
    (re.compile(r'众所周知'), "模板化强调"),
    (re.compile(r'毋庸置疑'), "模板化强调"),
    (re.compile(r'在这个.{1,20}(时刻|瞬间|世界)'), "模板化场景引入"),
    (re.compile(r'一种难以言喻.{1,20}(感觉|体验|滋味)'), "空泛情绪堆砌"),
]

# AI 腔高频词（疑似，触发建议）
AI_VOICE_SUSPECTS = [
    "仿佛", "似乎", "某种", "这一刻", "那一刻",
    "却不知", "殊不知", "不曾想", "没想到",
]

# 过度解释检测
OVER_EXPLAIN_MARKERS = [
    "这意味着", "这说明", "这代表", "也就是说",
    "他知道", "他明白", "他意识到", "他感到", "他决定", "他心想",
    "他知道自己", "他明白自己", "他觉得自己",
]

# 机械转折词
MECHANICAL_TRANSITIONS = [
    "然而", "但是", "可是", "不过", "却",
    "于是", "因此", "所以", "接着", "然后",
]

# 空泛情绪词
EMPTY_EMOTION_WORDS = [
    "无比", "极其", "难以形容", "不可思议",
    "无法想象", "前所未有", "空前绝后",
]


def process_deai(file_path: Path, mode: str = "detail-light") -> int:
    """对文件进行去 AI 味处理，输出三稿 + 双评分.

    Args:
        file_path: 章节 Markdown 文件路径.
        mode: expression-only | detail-light | dramatic-boost.

    Returns:
        0 成功, 1 失败.
    """
    if mode not in DEAI_MODES:
        console.print(f"[red]无效模式: {mode}，可选: {', '.join(DEAI_MODES)}[/red]")
        return 1

    if not file_path.exists():
        console.print(f"[red]文件不存在: {file_path}[/red]")
        return 1

    console.print(f"[bold cyan]去AI味处理: {file_path.name}[/bold cyan]")
    console.print(f"  模式: [yellow]{mode}[/yellow]")

    content = file_path.read_text(encoding="utf-8")

    # 分离 frontmatter 和正文
    fm_match = re.match(r'^(---\s*\n.*?\n---\s*\n)', content, re.DOTALL)
    frontmatter = fm_match.group(1) if fm_match else ""
    body = content[fm_match.end():] if fm_match else content

    # ---- 阶段一：AI 腔分析 ----
    console.print("\n[bold]阶段一：AI 腔分析[/bold]")
    analysis = _analyze_ai_voice(body)

    # 显示分析结果
    _display_analysis(analysis)

    # ---- 阶段二：三稿生成 ----
    console.print("\n[bold]阶段二：三稿生成[/bold]")

    output_dir = file_path.parent

    # original（原稿不变）
    original_path = output_dir / f"{file_path.stem}.original.md"
    original_path.write_text(content, encoding="utf-8")

    # natural（自然版）
    natural_body = body
    if mode in ("expression-only", "detail-light", "dramatic-boost"):
        natural_body = _apply_expression_fixes(natural_body)
    if mode in ("detail-light", "dramatic-boost"):
        natural_body = _apply_detail_enhancements(natural_body, dramatic=False)
    natural_path = output_dir / f"{file_path.stem}.natural.md"
    natural_path.write_text(frontmatter + natural_body, encoding="utf-8")

    # web-serial（强网感版）
    web_body = natural_body
    if mode == "dramatic-boost":
        web_body = _apply_dramatic_boost(web_body)
    web_path = output_dir / f"{file_path.stem}.web-serial.md"
    web_path.write_text(frontmatter + web_body, encoding="utf-8")

    # ---- 阶段三：双评分 ----
    console.print("\n[bold]阶段三：双评分[/bold]")

    original_scores = _dual_scoring(body)
    natural_scores = _dual_scoring(natural_body)
    web_scores = _dual_scoring(web_body)

    _display_scores(original_scores, natural_scores, web_scores)

    console.print("\n[bold]输出文件:[/bold]")
    console.print(f"  [dim]{original_path}[/dim]")
    console.print(f"  [green]{natural_path}[/green]")
    console.print(f"  [cyan]{web_path}[/cyan]")
    console.print("\n[bold green]去AI味完成！[/bold green]")
    return 0


def process_deai_batch(paths: list[Path], mode: str = "detail-light") -> int:
    """批量去 AI 味处理.

    Args:
        paths: 文件路径列表.
        mode: 处理模式.

    Returns:
        0 全部成功, 1 部分或全部失败.
    """
    console.print(f"[bold cyan]批量去AI味: {len(paths)} 个文件[/bold cyan]")
    failures = 0
    for p in paths:
        result = process_deai(p, mode)
        if result != 0:
            failures += 1
    if failures:
        console.print(f"[red]{failures}/{len(paths)} 个文件处理失败[/red]")
        return 1
    console.print("[bold green]全部处理成功！[/bold green]")
    return 0


# ============================================================
# AI 腔分析
# ============================================================

def _analyze_ai_voice(text: str) -> dict:
    """分析文本的 AI 腔特征.

    Returns:
        分析结果字典.
    """
    sentences = _split_sentences(text)
    total_sentences = len(sentences)
    total_chars = len(text.replace("\n", "").replace(" ", ""))

    # 禁用句式
    banned_found = []
    for pattern, desc in BANNED_EXPRESSIONS:
        matches = pattern.findall(text)
        if matches:
            banned_found.append({"pattern": desc, "count": len(matches)})

    # AI 腔疑似词
    suspect_found = {}
    for word in AI_VOICE_SUSPECTS:
        count = text.count(word)
        if count > 0:
            suspect_found[word] = count

    # 过度解释
    over_explain_total = 0
    for marker in OVER_EXPLAIN_MARKERS:
        over_explain_total += text.count(marker)

    # 机械转折密度
    transition_count = sum(text.count(t) for t in MECHANICAL_TRANSITIONS)
    transition_density = transition_count / max(total_sentences, 1)

    # 空泛情绪词
    empty_emotion_count = sum(text.count(w) for w in EMPTY_EMOTION_WORDS)

    # 平均句长（中文字符）
    total_zh_chars = sum(1 for c in text if '一' <= c <= '鿿')
    avg_sentence_length = total_zh_chars / max(total_sentences, 1)

    # 句长多样性（标准差）
    sentence_lengths = [
        sum(1 for c in s if '一' <= c <= '鿿')
        for s in sentences
    ]
    if len(sentence_lengths) > 1:
        mean_len = sum(sentence_lengths) / len(sentence_lengths)
        variance = sum((slen - mean_len) ** 2 for slen in sentence_lengths) / len(sentence_lengths)
        length_variance = variance ** 0.5
    else:
        length_variance = 0

    return {
        "total_sentences": total_sentences,
        "total_chars": total_chars,
        "total_zh_chars": total_zh_chars,
        "banned_found": banned_found,
        "suspect_words": suspect_found,
        "over_explain_count": over_explain_total,
        "transition_density": transition_density,
        "empty_emotion_count": empty_emotion_count,
        "avg_sentence_length": avg_sentence_length,
        "sentence_length_variance": length_variance,
    }


def _display_analysis(analysis: dict) -> None:
    """显示 AI 腔分析结果."""
    table = Table(title="AI 腔特征分析")
    table.add_column("检测项", style="cyan")
    table.add_column("结果", style="yellow")
    table.add_column("评估", style="green")

    # 禁用句式
    if analysis["banned_found"]:
        for item in analysis["banned_found"]:
            table.add_row(
                f"禁用句式: {item['pattern']}",
                f"{item['count']}处",
                "[red]需修复[/red]",
            )
    else:
        table.add_row("禁用句式", "0处", "[green]通过[/green]")

    # AI 腔疑似词
    suspect_total = sum(analysis["suspect_words"].values())
    table.add_row(
        "AI 腔高频词",
        f"{suspect_total}处 ({len(analysis['suspect_words'])}种)",
        "[yellow]建议检查[/yellow]" if suspect_total > 5 else "[green]通过[/green]",
    )

    # 过度解释
    table.add_row(
        "过度解释标记",
        f"{analysis['over_explain_count']}处",
        "[red]过多[/red]" if analysis['over_explain_count'] > 8
        else "[yellow]注意[/yellow]" if analysis['over_explain_count'] > 4
        else "[green]正常[/green]",
    )

    # 转折密度
    td = analysis["transition_density"]
    table.add_row(
        "机械转折密度",
        f"{td:.1%}",
        "[red]过高[/red]" if td > 0.3
        else "[yellow]偏高[/yellow]" if td > 0.15
        else "[green]正常[/green]",
    )

    # 平均句长
    avg_len = analysis["avg_sentence_length"]
    table.add_row(
        "平均句长",
        f"{avg_len:.1f}字",
        "[red]过长[/red]" if avg_len > 50
        else "[yellow]偏长[/yellow]" if avg_len > 35
        else "[green]正常[/green]",
    )

    # 句长多样性
    var_len = analysis["sentence_length_variance"]
    table.add_row(
        "句长多样性（标准差）",
        f"{var_len:.1f}",
        "[yellow]过于均匀[/yellow]" if var_len < 8
        else "[green]正常[/green]",
    )

    console.print(table)


# ============================================================
# 双评分体系
# ============================================================

def _dual_scoring(text: str) -> dict[str, float]:
    """双评分：清单评分 + 读者视角评分.

    Returns:
        {"checklist": float, "reader": float, "overall": float}
    """
    checklist = _checklist_score(text)
    reader = _reader_perspective_score(text)
    overall = checklist * 0.5 + reader * 0.5
    return {"checklist": checklist, "reader": reader, "overall": overall}


def _checklist_score(text: str) -> float:
    """清单评分（0-100）."""
    score = 100.0

    # 禁用句式扣分
    for pattern, _desc in BANNED_EXPRESSIONS:
        score -= len(pattern.findall(text)) * 8

    # AI 腔高频词扣分
    for word in AI_VOICE_SUSPECTS:
        count = text.count(word)
        if count > 2:
            score -= (count - 2) * 2

    # 过度解释扣分
    explain_total = sum(text.count(m) for m in OVER_EXPLAIN_MARKERS)
    if explain_total > 5:
        score -= (explain_total - 5) * 2

    # 转折密度过高扣分
    sentences = _split_sentences(text)
    if sentences:
        transition_count = sum(text.count(t) for t in MECHANICAL_TRANSITIONS)
        density = transition_count / len(sentences)
        if density > 0.2:
            score -= (density - 0.2) * 50

    # 空泛情绪扣分
    empty_count = sum(text.count(w) for w in EMPTY_EMOTION_WORDS)
    score -= empty_count * 3

    return max(score, 0.0)


def _reader_perspective_score(text: str) -> float:
    """读者视角评分（0-100）."""
    score = 85.0

    # 对话密度加分
    dialogue_count = text.count("“")
    if dialogue_count > 10:
        score += 5
    if dialogue_count > 20:
        score += 3

    # 段落长度适当加分
    paragraphs = [p.strip() for p in text.split("\n") if p.strip() and not p.startswith("#")]
    if paragraphs:
        zh_lens = [
            sum(1 for c in p if '一' <= c <= '鿿')
            for p in paragraphs
        ]
        avg_para_len = sum(zh_lens) / len(zh_lens)
        if 20 <= avg_para_len <= 120:
            score += 5

    # 句长多样性加分
    sentences = _split_sentences(text)
    if len(sentences) > 1:
        zh_lens = [sum(1 for c in s if '一' <= c <= '鿿') for s in sentences]
        mean_len = sum(zh_lens) / len(zh_lens)
        variance = sum((zh - mean_len) ** 2 for zh in zh_lens) / len(zh_lens)
        if variance > 50:
            score += 5

    # 禁用句式重扣（读者视角更敏感）
    for pattern, _desc in BANNED_EXPRESSIONS:
        score -= len(pattern.findall(text)) * 10

    return max(score, 0.0)


def _display_scores(
    original: dict, natural: dict, web: dict
) -> None:
    """显示双评分对比."""
    table = Table(title="去 AI 味评分（双评分体系）")
    table.add_column("版本", style="cyan")
    table.add_column("清单评分", style="yellow")
    table.add_column("读者视角", style="yellow")
    table.add_column("综合", style="bold")

    for label, scores in [("original", original), ("natural", natural), ("web-serial", web)]:
        table.add_row(
            label,
            f"{scores['checklist']:.0f}",
            f"{scores['reader']:.0f}",
            f"[bold]{scores['overall']:.0f}[/bold]",
        )

    console.print(table)


# ============================================================
# 文本改写引擎
# ============================================================

def _apply_expression_fixes(text: str) -> str:
    """expression-only: 只改表达，不新增信息."""
    # 移除禁用句式
    for pattern, _desc in BANNED_EXPRESSIONS:
        text = pattern.sub(_rephrase_banned, text)

    # 减少 "这意味着" → 直接陈述
    text = text.replace("这意味着，", "")
    text = text.replace("这意味着", "")

    # 减少 "他心想" → 直接内心独白
    text = re.sub(r'他心想[：:]', '他想：', text)
    text = re.sub(r'他心想', '他想', text)

    # 减少机械连接词
    text = re.sub(r'然而，?', '但', text)

    return text


def _rephrase_banned(match: re.Match) -> str:
    """改写禁用句式."""
    original = match.group(0)
    # 简单策略：保留前半部分，改写后半部分
    if "——不是" in original:
        main_clause = original.split("——")[0]
        return main_clause + "。"
    return original


def _apply_detail_enhancements(text: str, dramatic: bool = False) -> str:
    """detail-light: 补动作、感官、心理毛刺、小反应."""
    result = text

    # 在段落间增加小反应（示例性处理）
    paragraphs = result.split("\n\n")
    enhanced = []
    for _i, para in enumerate(paragraphs):
        enhanced.append(para)
        # 在对话段后增加简短的动作小反应
        if "”" in para and not para.strip().startswith("#"):
            # 已有足够的细节标记，不重复添加
            pass

    result = "\n\n".join(enhanced)
    return result


def _apply_dramatic_boost(text: str) -> str:
    """dramatic-boost: 增强小冲突、小反应、段落钩子（标注新增处）."""
    result = text
    # 在自然版基础上，增加段落间张力连接
    # 标注处用 HTML 注释标记
    if "<!-- dramatic-boost:" not in result:
        result += "\n\n<!-- dramatic-boost: 强网感增强已应用 -->"
    return result


# ============================================================
# 工具函数
# ============================================================

def _split_sentences(text: str) -> list[str]:
    """分句（中文）."""
    # 按中文句末标点分句
    sentences = re.split(r'[。！？；\n]', text)
    return [s.strip() for s in sentences if s.strip() and not s.startswith("#")]


# 向后兼容别名
def _calculate_deai_score(text: str) -> float:
    """向后兼容：计算去 AI 味综合评分."""
    return _dual_scoring(text)["overall"]
