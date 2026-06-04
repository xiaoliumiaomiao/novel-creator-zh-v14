"""仪表盘生成 — Markdown + HTML."""

from __future__ import annotations

from datetime import date

from rich.console import Console

from novel_creator.config import REPORTS_DIR, VAULT_DIR

console = Console()


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

    # Markdown 仪表盘
    md_content = f"""---
type: dashboard
updated: {today}
---

# 创作仪表盘

## 项目总览

| 项目 | 状态 | 章节数 | 总字数 | 均分 |
|------|------|--------|--------|------|
| sample-male | 示例 | 1 | 3120 | 87 |
| sample-female | 示例 | 1 | 3080 | 88 |

## 章节进度

| 项目 | 已规划 | 草稿 | 审阅中 | 去AI味 | 精修 | 已通过 |
|------|--------|------|--------|--------|------|--------|
| sample-male | 30 | 1 | 0 | 0 | 0 | 0 |
| sample-female | 30 | 1 | 0 | 0 | 0 | 0 |

## 字数统计

- 总有效字数：6200
- 平均每章：3100
- 字数达标率：100%

## 风险状态

- 风险触发次数：0
- 待处理风险：0
- 降险失败：0

## 评分趋势

_图表将在更多章节生成后展现_

## 伏笔状态

| 项目 | 新增 | 回收 | 待处理 |
|------|------|------|--------|
| sample-male | 0 | 0 | 0 |
| sample-female | 0 | 0 | 0 |

## Agent Trace 索引

_Agent Trace 将在创作期自动生成_

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
        <tr><td>sample-male</td><td>示例</td><td>1</td><td>3120</td><td>87</td></tr>
        <tr><td>sample-female</td><td>示例</td><td>1</td><td>3080</td><td>88</td></tr>
    </table>

    <h2>字数统计</h2>
    <p>总有效字数：6200 | 平均每章：3100 | 字数达标率：100%</p>

    <h2>风险状态</h2>
    <p>风险触发次数：0 | 待处理风险：0</p>

    <p><small>仪表盘自动生成</small></p>
</body>
</html>
"""

    html_path = REPORTS_DIR / "dashboard.html"
    html_path.write_text(html_content, encoding="utf-8")
    console.print(f"  [green]✓[/green] HTML 报表: {html_path}")

    console.print("\n[bold green]仪表盘生成完成！[/bold green]")
    return 0
