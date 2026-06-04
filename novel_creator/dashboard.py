"""仪表盘生成 — Markdown + HTML."""

from __future__ import annotations

from datetime import date
from pathlib import Path
from typing import Any

from rich.console import Console

from novel_creator.config import REPORTS_DIR, VAULT_DIR
from novel_creator.linting import _count_effective_chars, _extract_body, _parse_frontmatter

console = Console()

DEAI_VARIANT_SUFFIXES = (".original.md", ".natural.md", ".web-serial.md")


def generate_dashboard() -> int:
    """生成 Markdown 仪表盘和 HTML 报表.

    Returns:
        0 成功, 1 失败.
    """
    console.print("[bold cyan]生成仪表盘...[/bold cyan]")

    # 确保目录存在
    dashboard_dir = VAULT_DIR / "00_Dashboard"
    dashboard_dir.mkdir(parents=True, exist_ok=True)
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)

    today = date.today().isoformat()
    projects = _collect_projects()
    total_words = sum(project["words"] for project in projects)
    total_chapters = sum(project["chapters"] for project in projects)
    avg_words = round(total_words / total_chapters) if total_chapters else 0
    pass_rate = _format_percent(
        sum(1 for chapter in _chapter_files() if _chapter_word_count(chapter) >= 2500)
        / total_chapters
        if total_chapters
        else 0
    )
    trace_files = sorted((VAULT_DIR / "00_Dashboard" / "Agent_Traces").glob("*.md"))
    reference_cards = [
        path for path in (VAULT_DIR / "References").rglob("*.md")
        if path.name != "README.md"
    ] if (VAULT_DIR / "References").exists() else []

    project_rows = "\n".join(
        f"| {p['book']} | 示例 | {p['chapters']} | {p['words']} | {p['score']} |"
        for p in projects
    ) or "| 暂无 | - | 0 | 0 | - |"

    progress_rows = "\n".join(
        "| {book} | {planned} | {drafted} | {reviewed} | {deai} | {polished} | {approved} |".format(
            **p
        )
        for p in projects
    ) or "| 暂无 | 0 | 0 | 0 | 0 | 0 | 0 |"

    foreshadow_rows = "\n".join(
        f"| {p['book']} | 0 | 0 | 0 |" for p in projects
    ) or "| 暂无 | 0 | 0 | 0 |"

    trace_links = "\n".join(
        f"- [[Agent_Traces/{path.stem}|{path.stem}]]" for path in trace_files
    ) or "_Agent Trace 将在创作期自动生成_"

    # Markdown 仪表盘
    md_content = f"""---
type: dashboard
updated: {today}
---

# 创作仪表盘

## 项目总览

| 项目 | 状态 | 章节数 | 总字数 | 均分 |
|------|------|--------|--------|------|
{project_rows}

## 章节进度

| 项目 | 已规划 | 草稿 | 审阅中 | 去AI味 | 精修 | 已通过 |
|------|--------|------|--------|--------|------|--------|
{progress_rows}

## 字数统计

- 总有效字数：{total_words}
- 平均每章：{avg_words}
- 字数达标率：{pass_rate}

## 风险状态

- 风险触发次数：0
- 待处理风险：0
- 降险失败：0

## 评分趋势

_图表将在更多章节生成后展现_

## 伏笔状态

| 项目 | 新增 | 回收 | 待处理 |
|------|------|------|--------|
{foreshadow_rows}

## Agent Trace 索引

{trace_links}

## 参考库结构卡统计

- 结构卡数量：{len(reference_cards)}
- IMA 接入状态：已配置

---
*仪表盘自动生成于 {today}*
"""

    dashboard_md = dashboard_dir / "Dashboard.md"
    dashboard_md.write_text(md_content, encoding="utf-8")
    console.print(f"  [green]✓[/green] Markdown 仪表盘: {dashboard_md}")

    # HTML 报表
    html_content = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="utf-8">
    <title>创作仪表盘 — Novel Creator ZH V14</title>
    <style>
        body {{
            font-family: system-ui, sans-serif;
            max-width: 900px; margin: 0 auto;
            padding: 2rem; background: #1a1a2e; color: #e0e0e0;
        }}
        h1 {{
            color: #00d4ff;
            border-bottom: 2px solid #00d4ff;
            padding-bottom: 0.5rem;
        }}
        h2 {{ color: #ff6b6b; margin-top: 2rem; }}
        table {{ border-collapse: collapse; width: 100%; margin: 1rem 0; }}
        th, td {{ border: 1px solid #333; padding: 0.5rem 1rem; text-align: left; }}
        th {{ background: #16213e; color: #00d4ff; }}
        td {{ background: #0f3460; }}
        .pass {{ color: #4ecca3; }}
        .fail {{ color: #ff6b6b; }}
    </style>
</head>
<body>
    <h1>创作仪表盘</h1>
    <p>更新于：{today}</p>

    <h2>项目总览</h2>
    <table>
        <tr><th>项目</th><th>状态</th><th>章节数</th><th>总字数</th><th>均分</th></tr>
        {_html_project_rows(projects)}
    </table>

    <h2>字数统计</h2>
    <p>总有效字数：{total_words} | 平均每章：{avg_words} | 字数达标率：{pass_rate}</p>

    <h2>风险状态</h2>
    <p>风险触发次数：0 | 待处理风险：0</p>

    <h2>Agent Trace</h2>
    <p>Trace 文件数：{len(trace_files)}</p>

    <h2>参考库结构卡</h2>
    <p>结构卡数量：{len(reference_cards)}</p>

    <p><small>仪表盘自动生成</small></p>
</body>
</html>
"""

    html_path = REPORTS_DIR / "dashboard.html"
    html_path.write_text(html_content, encoding="utf-8")
    console.print(f"  [green]✓[/green] HTML 报表: {html_path}")

    console.print("\n[bold green]仪表盘生成完成！[/bold green]")
    return 0


def _chapter_files() -> list[Path]:
    samples_dir = VAULT_DIR / "Samples"
    chapters_dir = VAULT_DIR / "05_Chapters"
    files: list[Path] = []
    for directory in (samples_dir, chapters_dir):
        if directory.exists():
            files.extend(directory.rglob("第*章 *.md"))
    return [
        path for path in files
        if not path.name.endswith(DEAI_VARIANT_SUFFIXES)
    ]


def _chapter_word_count(path: Path) -> int:
    content = path.read_text(encoding="utf-8")
    body = _extract_body(content)
    return _count_effective_chars(body)


def _collect_projects() -> list[dict[str, Any]]:
    grouped: dict[str, dict[str, Any]] = {}
    for path in _chapter_files():
        content = path.read_text(encoding="utf-8")
        metadata = _parse_frontmatter(content)
        book = str(metadata.get("book") or path.parent.name)
        project = grouped.setdefault(
            book,
            {
                "book": book,
                "chapters": 0,
                "words": 0,
                "scores": [],
                "planned": 0,
                "drafted": 0,
                "reviewed": 0,
                "deai": 0,
                "polished": 0,
                "approved": 0,
            },
        )
        status = metadata.get("status", "drafted")
        if status in project:
            project[status] += 1
        project["chapters"] += 1
        project["words"] += _chapter_word_count(path)

        score_values = [
            metadata.get("commercial_score"),
            metadata.get("continuity_score"),
            metadata.get("deai_score"),
        ]
        numeric_scores = [float(score) for score in score_values if isinstance(score, int | float)]
        if numeric_scores:
            project["scores"].append(round(sum(numeric_scores) / len(numeric_scores)))

    projects = []
    for project in grouped.values():
        scores = project.pop("scores")
        project["score"] = round(sum(scores) / len(scores)) if scores else "-"
        projects.append(project)
    return sorted(projects, key=lambda item: item["book"])


def _format_percent(value: float) -> str:
    return f"{value * 100:.0f}%"


def _html_project_rows(projects: list[dict[str, Any]]) -> str:
    if not projects:
        return "<tr><td>暂无</td><td>-</td><td>0</td><td>0</td><td>-</td></tr>"
    return "\n        ".join(
        f"<tr><td>{p['book']}</td><td>示例</td><td>{p['chapters']}</td>"
        f"<td>{p['words']}</td><td>{p['score']}</td></tr>"
        for p in projects
    )
