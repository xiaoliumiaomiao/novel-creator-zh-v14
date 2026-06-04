"""硬规则检查器 — YAML, 双链, 字数, 格式, 英文比例, 禁用句式, 风险, 参考库保护."""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any

from rich.console import Console

from novel_creator.config import (
    CHAPTER_MAX_WORDS,
    CHAPTER_MIN_WORDS,
    MAX_ENGLISH_RATIO,
    PARAGRAPH_MAX_CHARS,
    VAULT_DIR,
)

console = Console()

# 禁用句式正则
BANNED_PATTERNS = [
    (re.compile(r'——不是[^，。；\n]{1,30}[，。；]'), "「A——不是B」式模板句"),
    (re.compile(r'这意味着'), "过度解释腔：这意味着"),
    (re.compile(r'总而言之'), "机械总结腔：总而言之"),
    (re.compile(r'综上所述'), "机械总结腔：综上所述"),
    (re.compile(r'不难看出'), "解释腔：不难看出"),
    (re.compile(r'毋庸置疑'), "模板化强调：毋庸置疑"),
    (re.compile(r'众所周知'), "模板化强调：众所周知"),
]


def run_lint() -> int:
    """运行完整硬规则检查，扫描所有 vault 章节.

    Returns:
        0 全部通过, 1 存在问题.
    """
    console.print("[bold cyan]运行硬规则检查...[/bold cyan]\n")

    total_issues = 0

    # 扫描章节文件
    chapters_dir = VAULT_DIR / "05_Chapters"
    samples_dir = VAULT_DIR / "Samples"

    all_md_files: list[Path] = []
    for directory in [chapters_dir, samples_dir]:
        if directory.exists():
            all_md_files.extend(directory.rglob("*.md"))

    if not all_md_files:
        console.print("[yellow]未找到章节文件[/yellow]")
        # 也检查样例
        return 0

    for md_file in all_md_files:
        issues = _check_file(md_file)
        total_issues += len(issues)

        if issues:
            console.print(f"[yellow]⚠ {md_file.relative_to(VAULT_DIR.parent)}[/yellow]")
            for issue in issues:
                console.print(f"    [red]✗[/red] {issue}")
        else:
            console.print(f"[green]✓[/green] {md_file.relative_to(VAULT_DIR.parent)}")

    # 参考库保护检查
    ref_issues = _check_reference_protection()
    total_issues += ref_issues

    # 汇总
    result_msg = (
        "[bold green]全部通过！" if total_issues == 0
        else f"[bold red]发现 {total_issues} 个问题[/bold red]"
    )
    console.print(f"\n{result_msg}")
    return 1 if total_issues > 0 else 0


def run_publish_check() -> int:
    """发布前总闸门检查.

    Returns:
        0 通过, 1 未通过.
    """
    console.print("[bold cyan]发布前总闸门检查...[/bold cyan]\n")

    # 运行所有检查
    lint_result = run_lint()

    # 额外检查
    # Agent Trace 检查
    trace_dir = VAULT_DIR / "00_Dashboard" / "Agent_Traces"
    if trace_dir.exists() and list(trace_dir.iterdir()):
        console.print("[green]✓[/green] Agent Trace 存在")
    else:
        console.print("[yellow]⚠[/yellow] Agent Trace 目录为空（创作期自动生成）")

    # 参考库泄漏检查
    ref_dir = VAULT_DIR / "References"
    if ref_dir.exists():
        md_files = list(ref_dir.rglob("*.md"))
        md_files = [f for f in md_files if f.name != "README.md"]
        if md_files:
            console.print(f"[dim]参考库: {len(md_files)} 个文件（不参与发布检查）[/dim]")

    if lint_result == 0:
        console.print("\n[bold green]发布检查通过！[/bold green]")
        return 0
    else:
        console.print("\n[bold red]发布检查未通过，请修复上述问题[/bold red]")
        return 1


def _check_file(file_path: Path) -> list[str]:
    """检查单个文件，返回问题列表."""
    issues: list[str] = []

    try:
        content = file_path.read_text(encoding="utf-8")
    except Exception as e:
        return [f"无法读取文件: {e}"]

    # 1. YAML properties
    if not content.startswith("---"):
        issues.append("缺少 YAML frontmatter")
    else:
        metadata = _parse_frontmatter(content)
        if not metadata:
            issues.append("YAML frontmatter 为空")

    # 2. 提取正文
    body = _extract_body(content)

    # 3. 有效字数
    effective_words = _count_effective_chars(body)

    # 判断是否为正文章节（非设定文档）
    is_chapter_body = bool(re.search(r'第\d+章', content))

    if is_chapter_body:
        if effective_words < CHAPTER_MIN_WORDS:
            issues.append(f"有效字数不足: {effective_words}/{CHAPTER_MIN_WORDS}")
        elif effective_words > CHAPTER_MAX_WORDS:
            issues.append(f"有效字数超标: {effective_words}/{CHAPTER_MAX_WORDS}")

    # 4. 英文比例（仅正文检查）
    if is_chapter_body and body.strip():
        total_chars = len([c for c in body if not c.isspace()])
        if total_chars > 0:
            english_chars = sum(1 for c in body if c.isascii() and c.isalpha())
            english_ratio = english_chars / total_chars
            if english_ratio > MAX_ENGLISH_RATIO:
                issues.append(f"英文比例超标: {english_ratio:.2%} > {MAX_ENGLISH_RATIO:.0%}")

    # 5. 标题格式
    if is_chapter_body:
        title_match = re.search(r'^# 第(\d+)章 (.+)$', body, re.MULTILINE)
        if not title_match:
            issues.append("章节标题格式不正确（应为: # 第N章 标题）")

    # 6. 文件名格式
    if is_chapter_body and not re.match(r'第\d+章 .+\.md$', file_path.name):
        issues.append(f"文件名格式不正确: {file_path.name}（应为: 第N章 标题.md）")

    # 7. 空行检查（仅正文）
    if is_chapter_body:
        body_lines = body.split("\n")
        for i, line in enumerate(body_lines):
            if line.strip() == "" and i > 0 and body_lines[i - 1].strip() == "":
                issues.append(f"发现连续空行（第{i + 1}行附近）")
                break

    # 8. 段落长度
    paragraphs = [p.strip() for p in body.split("\n") if p.strip() and not p.startswith("#")]
    for i, para in enumerate(paragraphs):
        if _count_effective_chars(para) > PARAGRAPH_MAX_CHARS:
            para_chars = _count_effective_chars(para)
            issues.append(
                f"段落过长: {para_chars}字（上限{PARAGRAPH_MAX_CHARS}字，第{i + 1}段）"
            )
            break  # 每个文件只报告一次

    # 9. 中文标点（正文）
    if is_chapter_body and body.strip():
        # 检查英文句号作为句尾
        english_periods = re.findall(r'[a-zA-Z]\.', body)
        if english_periods:
            issues.append("发现英文句号及前导字母组合")

    # 10. 禁用句式
    for pattern, desc in BANNED_PATTERNS:
        matches = pattern.findall(body)
        if matches:
            issues.append(f"触发禁用句式: {desc}（{len(matches)}处）")

    # 11. 中文引号
    if is_chapter_body and '"' in body:
        # 检查是否有未配对的英文引号
        issues.append("发现英文双引号，应使用中文引号「""」")

    # 12. Obsidian 双链扫描
    wikilinks = _scan_wikilinks(content)
    if wikilinks:
        broken = _validate_wikilinks(wikilinks, file_path)
        for link in broken:
            issues.append(f"Obsidian 双链目标不存在: [[{link}]]")

    return issues


def _check_reference_protection() -> int:
    """检查参考库是否受到保护."""
    ref_dir = VAULT_DIR / "References"
    if not ref_dir.exists():
        return 0

    issues = 0
    # 检查是否有被 git 追踪的参考库文件
    import subprocess
    try:
        result = subprocess.run(
            ["git", "ls-files", "--error-unmatch", str(ref_dir) + "/"],
            capture_output=True, text=True, cwd=VAULT_DIR.parent,
        )
        if result.returncode == 0 and result.stdout.strip():
            console.print("[red]✗[/red] 参考库文件被 Git 追踪！")
            issues += 1
    except Exception:
        pass

    return issues


def _parse_frontmatter(content: str) -> dict[str, Any]:
    """解析 YAML frontmatter."""
    import yaml
    match = re.match(r'^---\s*\n(.*?)\n---', content, re.DOTALL)
    if not match:
        return {}
    try:
        return yaml.safe_load(match.group(1)) or {}
    except yaml.YAMLError:
        return {}


def _extract_body(content: str) -> str:
    """提取正文."""
    return re.sub(r'^---\s*\n.*?\n---\s*\n', '', content, flags=re.DOTALL)


def _count_effective_chars(text: str) -> int:
    """统计有效中文字符和数字."""
    count = 0
    for char in text:
        if '一' <= char <= '鿿' or '㐀' <= char <= '䶿' or char.isdigit():
            count += 1
    return count


# Obsidian wikilink 正则: [[target]], [[target|alias]], [[target#heading]]
_WIKILINK_RE = re.compile(r'\[\[([^\]|#]+)(?:[|#][^\]]+)?\]\]')


def _scan_wikilinks(content: str) -> list[str]:
    """扫描内容中的所有 Obsidian 双链目标.

    Args:
        content: Markdown 内容.

    Returns:
        去重后的目标页面名列表.
    """
    targets = _WIKILINK_RE.findall(content)
    # 去重并去除首尾空白
    seen: set[str] = set()
    result: list[str] = []
    for t in targets:
        t = t.strip()
        if t and t not in seen:
            seen.add(t)
            result.append(t)
    return result


def _validate_wikilinks(targets: list[str], source_file: Path) -> list[str]:
    """验证双链目标是否存在.

    在 vault 中搜索对应的 .md 文件。

    Args:
        targets: 双链目标页面名列表.
        source_file: 源文件路径.

    Returns:
        无法解析的链接列表.
    """
    from novel_creator.config import VAULT_DIR

    broken: list[str] = []
    for target in targets:
        found = False
        # 在 vault 中搜索匹配的 .md 文件
        for md_file in VAULT_DIR.rglob("*.md"):
            if md_file.stem == target and md_file != source_file:
                found = True
                break
        if not found:
            broken.append(target)
    return broken
