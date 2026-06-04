"""风险审查 — 法律、政治、平台安全."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from rich.console import Console
from rich.panel import Panel

console = Console()

# 高风险关键词（简化版，实际由 risk Agent 深度审查）
HIGH_RISK_KEYWORDS: dict[str, list[str]] = {
    "政治风险": ["习近平", "中共", "中国", "政府", "国家", "党", "领导人"],
    "涉黄风险": ["呻吟", "赤裸", "床第", "欢好"],
    "赌博风险": ["赌场", "赌博", "押注", "赌局"],
    "毒品风险": ["毒品", "吸毒", "白粉", "海洛因", "冰毒", "大麻"],
    "暴恐风险": ["恐怖", "爆炸", "屠杀", "血腥镇压"],
}


def review_file(file_path: Path) -> dict[str, Any]:
    """审查单个文件的风险.

    Args:
        file_path: 文件路径.

    Returns:
        风险审查报告字典.
    """
    if not file_path.exists():
        return {"pass": False, "error": "文件不存在"}

    content = file_path.read_text(encoding="utf-8")
    findings: list[dict[str, str]] = []

    # 逐类检查
    for risk_type, keywords in HIGH_RISK_KEYWORDS.items():
        for keyword in keywords:
            if keyword in content:
                # 找到具体位置
                idx = content.find(keyword)
                line_num = content[:idx].count("\n") + 1
                findings.append({
                    "type": risk_type,
                    "keyword": keyword,
                    "line": str(line_num),
                    "context": content[max(0, idx - 20):idx + len(keyword) + 20],
                })

    report: dict[str, Any] = {
        "pass": len(findings) == 0,
        "findings": findings,
        "file": str(file_path),
    }

    return report


def review_and_mitigate(file_path: Path, max_rounds: int = 2) -> dict[str, Any]:
    """审查并尝试自动降险.

    Args:
        file_path: 文件路径.
        max_rounds: 最大自动降险轮数.

    Returns:
        最终审查报告.
    """
    console.print(f"[bold cyan]风险审查: {file_path.name}[/bold cyan]")

    round_num = 0
    current_report = review_file(file_path)

    while not current_report["pass"] and round_num < max_rounds:
        round_num += 1
        console.print(f"  [yellow]第{round_num}轮降险...[/yellow]")

        # 自动降险：标记风险位置
        content = file_path.read_text(encoding="utf-8")
        mitigated = False

        for finding in current_report["findings"]:
            risk_type = finding["type"]
            keyword = finding["keyword"]
            line = finding["line"]
            # 在风险处添加审查注释（不影响正文，仅标记）
            if f"<!-- risk:{risk_type}:{keyword} -->" not in content:
                lines = content.split("\n")
                target_line = int(line) - 1
                if 0 <= target_line < len(lines):
                    lines[target_line] = (
                        f"<!-- risk-review: {risk_type} | 关键词: {keyword} | "
                        f"状态: 待人工审查 -->\n{lines[target_line]}"
                    )
                    mitigated = True
                content = "\n".join(lines)

        if mitigated:
            # 写入带标记的版本
            marked_path = file_path.parent / f"{file_path.stem}.risk-marked{file_path.suffix}"
            marked_path.write_text(content, encoding="utf-8")

        current_report = review_file(file_path)

    # 最终报告
    if current_report["pass"]:
        console.print("  [green]✓ 风险审查通过[/green]")
    else:
        console.print(f"  [red]✗ 风险审查未通过（已尝试{round_num}轮自动降险）[/red]")
        for finding in current_report["findings"]:
            finding_info = (
                f"    [red]•[/red] {finding['type']}: "
                f"「{finding['keyword']}」第{finding['line']}行"
            )
            console.print(finding_info)

    return current_report


def print_risk_report(report: dict[str, Any]) -> None:
    """打印格式化的风险报告."""
    if report.get("pass"):
        console.print(Panel("[green]风险审查通过[/green]", title="风险报告"))
        return

    lines = [
        "通过状态: [red]未通过[/red]",
        f"文件: {report.get('file', 'N/A')}",
        "",
    ]
    for finding in report.get("findings", []):
        lines.append(f"风险类型: [red]{finding['type']}[/red]")
        lines.append(f"关键词: {finding['keyword']}")
        lines.append(f"位置: 第{finding['line']}行")
        lines.append(f"上下文: ...{finding['context']}...")
        lines.append("---")

    console.print(Panel("\n".join(lines), title="风险报告"))
