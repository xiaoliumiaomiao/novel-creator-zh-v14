"""去 AI 味系统 — expression-only, detail-light, dramatic-boost 三种模式."""

from __future__ import annotations

from pathlib import Path

from rich.console import Console

from novel_creator.config import DEAI_MODES

console = Console()

# AI 腔特征标记
AI_VOICE_MARKERS = [
    "——不是",
    "这意味着",
    "总而言之",
    "综上所述",
    "不难看出",
    "毋庸置疑",
    "众所周知",
    "在这个",
    "在这一刻",
    "仿佛",
    "似乎",
    "某种",
    "一种难以言喻",
]

# 过度解释句式
OVER_EXPLAIN_PATTERNS = [
    "他知道",
    "他明白",
    "他意识到",
    "他感到",
    "他决定",
    "他心想",
]


def process_deai(file_path: Path, mode: str = "detail-light") -> int:
    """对文件进行去 AI 味处理，输出三稿.

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
    import re
    fm_match = re.match(r'^(---\s*\n.*?\n---\s*\n)', content, re.DOTALL)
    frontmatter = fm_match.group(1) if fm_match else ""
    body = content[fm_match.end():] if fm_match else content

    # 分析 AI 腔
    console.print("\n[bold]AI 腔分析:[/bold]")
    issues_found = 0
    for marker in AI_VOICE_MARKERS:
        count = body.count(marker)
        if count > 0:
            console.print(f"  [yellow]⚠[/yellow] 发现「{marker}」: {count}处")
            issues_found += count

    for marker in OVER_EXPLAIN_PATTERNS:
        count = body.count(marker)
        if count > 3:
            console.print(f"  [yellow]⚠[/yellow] 过度使用「{marker}」: {count}处")
            issues_found += 1

    if issues_found == 0:
        console.print("  [green]✓[/green] 未检测到明显 AI 腔特征")

    # 生成三稿
    output_dir = file_path.parent

    # original（原稿不变）
    original_path = output_dir / f"{file_path.stem}.original.md"
    original_path.write_text(content, encoding="utf-8")

    # natural（自然版）
    natural_body = _apply_expression_fixes(body)
    natural_path = output_dir / f"{file_path.stem}.natural.md"
    natural_path.write_text(frontmatter + natural_body, encoding="utf-8")

    # web-serial（强网感版）
    web_serial_body = natural_body
    if mode in ("detail-light", "dramatic-boost"):
        web_serial_body = _apply_detail_boost(web_serial_body, mode == "dramatic-boost")
    web_path = output_dir / f"{file_path.stem}.web-serial.md"
    web_path.write_text(frontmatter + web_serial_body, encoding="utf-8")

    # 评分
    original_score = _calculate_deai_score(body)
    natural_score = _calculate_deai_score(natural_body)
    web_score = _calculate_deai_score(web_serial_body)

    console.print("\n[bold]去AI味评分:[/bold]")
    console.print(f"  original: [yellow]{original_score:.0f}[/yellow]")
    console.print(f"  natural:  [green]{natural_score:.0f}[/green]")
    console.print(f"  web-serial: [green]{web_score:.0f}[/green]")

    console.print("\n[bold]输出文件:[/bold]")
    console.print(f"  [dim]{original_path}[/dim]")
    console.print(f"  [green]{natural_path}[/green]")
    console.print(f"  [cyan]{web_path}[/cyan]")

    console.print("\n[bold green]去AI味完成！[/bold green]")
    return 0


def _apply_expression_fixes(text: str) -> str:
    """应用表达层面修复（expression-only 级别）."""
    # 替换 "——不是" 模式
    import re
    text = re.sub(r'(.)——不是[^，。；\n]{1,40}[，。；]', r'\1，', text)

    # 移除机械总结
    for phrase in ["总而言之，", "综上所述，", "毋庸置疑，", "众所周知，"]:
        text = text.replace(phrase, "")

    # 减少 "这意味着"
    text = text.replace("这意味着", "这说明")

    return text


def _apply_detail_boost(text: str, dramatic: bool = False) -> str:
    """应用细节增强（detail-light / dramatic-boost）.

    注：此为自动化标记版本，实际创作中由 anti-ai-voice-editor Agent 执行。
    dramatic=True 时标注新增处。
    """
    # 简化处理：标注可增强位置
    # 实际完整实现在 anti-ai-voice-editor Agent 中
    if dramatic and "【dramatic-boost 增强标记】" not in text:
        text += "\n\n<!-- dramatic-boost: 已标注增强位置 -->"

    return text


def _calculate_deai_score(text: str) -> float:
    """计算去 AI 味评分."""
    score = 90.0

    for marker in AI_VOICE_MARKERS:
        count = text.count(marker)
        if count > 0:
            score -= count * 3

    for marker in OVER_EXPLAIN_PATTERNS:
        count = text.count(marker)
        if count > 3:
            score -= (count - 3) * 2

    return max(score, 0.0)
