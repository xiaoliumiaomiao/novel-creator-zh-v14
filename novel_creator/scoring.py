"""章节评分 — 商业节奏、连续性、人物动机、去 AI 味、风险."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from rich.console import Console
from rich.table import Table

from novel_creator.config import (
    CHAPTER_MAX_WORDS,
    CHAPTER_MIN_WORDS,
    MAX_ENGLISH_RATIO,
    PARAGRAPH_MAX_CHARS,
    QUALITY_THRESHOLD,
)

console = Console()


def score_chapter(file_path: Path) -> int:
    """对章节文件进行多维度评分.

    Args:
        file_path: 章节 Markdown 文件路径.

    Returns:
        0 通过, 1 未通过.
    """
    if not file_path.exists():
        console.print(f"[red]文件不存在: {file_path}[/red]")
        return 1

    content = file_path.read_text(encoding="utf-8")

    # 解析 YAML frontmatter
    metadata = _parse_frontmatter(content)
    # 提取正文（去除 YAML 和标题）
    body = _extract_body(content)

    scores: dict[str, Any] = {}

    # 字数和格式评分
    effective_words = _count_effective_chars(body)
    scores["effective_word_count"] = effective_words

    word_score = _score_word_count(effective_words)
    scores["word_count_score"] = word_score

    # 英文比例
    english_ratio = _calc_english_ratio(body)
    scores["english_ratio"] = english_ratio

    # 段落检查
    para_issues = _check_paragraphs(body)
    scores["paragraph_issues"] = len(para_issues)

    # 空行检查
    empty_lines = _check_empty_lines(body)
    scores["empty_line_issues"] = len(empty_lines)

    # 基础分（从 metadata 读取或计算）
    commercial = metadata.get("commercial_score", _estimate_commercial_score(body, effective_words))
    continuity = metadata.get("continuity_score", 85)
    deai = metadata.get("deai_score", _estimate_deai_score(body))
    risk = metadata.get("risk_status", "pass")

    scores["commercial_score"] = commercial
    scores["continuity_score"] = continuity
    scores["deai_score"] = deai
    scores["risk_status"] = risk

    # 综合评分
    overall = (commercial * 0.35 + continuity * 0.25 + deai * 0.25 + word_score * 0.15)

    # 显示评分表
    table = Table(title=f"章节评分: {file_path.name}")
    table.add_column("维度", style="cyan")
    table.add_column("得分", style="yellow")
    table.add_column("说明", style="dim")

    table.add_row("有效字数", str(effective_words), _word_range_desc(effective_words))
    table.add_row("字数评分", f"{word_score:.0f}", "")
    eng_status = "超标" if english_ratio > MAX_ENGLISH_RATIO else "通过"
    table.add_row("英文比例", f"{english_ratio:.2%}", eng_status)
    table.add_row("商业节奏", f"{commercial:.0f}", "")
    table.add_row("连续性", f"{continuity:.0f}", "")
    table.add_row("去AI味", f"{deai:.0f}", "")
    table.add_row("风险状态", risk, "")
    table.add_row("段落问题", str(len(para_issues)), "")
    table.add_row("空行问题", str(len(empty_lines)), "")
    table.add_row("综合评分", f"[bold]{overall:.0f}[/bold]", "")

    console.print(table)

    passed = overall >= QUALITY_THRESHOLD
    if passed:
        console.print(f"[bold green]✓ 通过（≥{QUALITY_THRESHOLD}分）[/bold green]")
    else:
        console.print(f"[bold red]✗ 未通过（<{QUALITY_THRESHOLD}分）[/bold red]")

    return 0 if passed else 1


def _parse_frontmatter(content: str) -> dict[str, Any]:
    """解析 YAML frontmatter."""
    import re

    import yaml

    match = re.match(r'^---\s*\n(.*?)\n---', content, re.DOTALL)
    if not match:
        return {}
    try:
        return yaml.safe_load(match.group(1)) or {}
    except yaml.YAMLError:
        return {}


def _extract_body(content: str) -> str:
    """提取正文（去除 YAML frontmatter）."""
    import re
    return re.sub(r'^---\s*\n.*?\n---\s*\n', '', content, flags=re.DOTALL)


def _count_effective_chars(text: str) -> int:
    """统计有效中文字符和数字."""
    count = 0
    for char in text:
        if '一' <= char <= '鿿' or '㐀' <= char <= '䶿' or char.isdigit():
            count += 1
    return count


def _calc_english_ratio(text: str) -> float:
    """计算英文字母占比."""
    total_chars = len([c for c in text if not c.isspace()])
    if total_chars == 0:
        return 0.0
    english_chars = sum(1 for c in text if c.isascii() and c.isalpha())
    return english_chars / total_chars


def _check_paragraphs(text: str) -> list[int]:
    """检查超长段落，返回问题段落长度列表."""
    issues = []
    paragraphs = [p.strip() for p in text.split("\n") if p.strip()]
    for para in paragraphs:
        effective = _count_effective_chars(para)
        if effective > PARAGRAPH_MAX_CHARS:
            issues.append(effective)
    return issues


def _check_empty_lines(text: str) -> list[int]:
    """检查完全空行."""
    issues = []
    lines = text.split("\n")
    for i, line in enumerate(lines):
        if i == len(lines) - 1 and line == "":
            continue
        if line == "" and i > 0:  # 连续空行
            issues.append(i)
    return issues


def _score_word_count(count: int) -> float:
    """字数字评分."""
    if CHAPTER_MIN_WORDS <= count <= CHAPTER_MAX_WORDS:
        return 100.0
    elif count < CHAPTER_MIN_WORDS:
        return max(0, 100 - (CHAPTER_MIN_WORDS - count) * 0.1)
    else:
        return max(0, 100 - (count - CHAPTER_MAX_WORDS) * 0.05)


def _word_range_desc(count: int) -> str:
    """字数范围描述."""
    if count < CHAPTER_MIN_WORDS:
        return f"不足（差{CHAPTER_MIN_WORDS - count}字）"
    elif count > CHAPTER_MAX_WORDS:
        return f"超标（多{count - CHAPTER_MAX_WORDS}字）"
    else:
        return "合格"


def _estimate_commercial_score(body: str, word_count: int) -> float:
    """估算商业节奏分（简化版）."""
    score = 80.0
    # 字数在范围内加 5 分
    if CHAPTER_MIN_WORDS <= word_count <= CHAPTER_MAX_WORDS:
        score += 5
    # 检查是否有对话（对话密度）
    dialogue_count = body.count("“")
    if dialogue_count > 10:
        score += 3
    # 段落适中加分
    paragraphs = [p for p in body.split("\n") if p.strip()]
    if paragraphs and _count_effective_chars("".join(paragraphs)) / len(paragraphs) < 150:
        score += 2
    return min(score, 100.0)


def _estimate_deai_score(body: str) -> float:
    """估算去 AI 味评分（简化版）."""
    score = 85.0
    # 检查禁用句式
    if "——不是" in body:
        score -= 20
    # 检查过度解释的提示词
    over_explain_markers = ["这意味着", "总而言之", "综上所述", "不难看出"]
    for marker in over_explain_markers:
        if marker in body:
            score -= 5
    return max(score, 0.0)
