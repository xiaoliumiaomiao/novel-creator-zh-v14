"""Git 同步 — 安全分支推送."""

from __future__ import annotations

import subprocess
import sys

from rich.console import Console

from novel_creator.config import PROJECT_ROOT

console = Console()


def git_sync() -> int:
    """安全 Git 同步流程.

    1. 运行测试
    2. 运行 lint
    3. 检查当前分支
    4. 禁止直推主干
    5. 检测 origin
    6. 中文 commit
    7. push

    Returns:
        0 成功, 1 失败.
    """
    console.print("[bold cyan]Git 同步...[/bold cyan]\n")

    # 1. 前置检查：测试和 lint
    console.print("[bold]步骤 1/5: 运行测试...[/bold]")
    try:
        result = subprocess.run(
            [sys.executable, "-m", "pytest", "--tb=short"],
            capture_output=True, text=True, cwd=str(PROJECT_ROOT),
            timeout=60,
        )
        if result.returncode != 0:
            console.print("[red]测试未通过，停止同步[/red]")
            console.print(result.stdout[-500:] if result.stdout else "")
            console.print(result.stderr[-500:] if result.stderr else "")
            return 1
        console.print("  [green]✓[/green] 测试通过")
    except subprocess.TimeoutExpired:
        console.print("[red]测试超时[/red]")
        return 1
    except FileNotFoundError:
        console.print("[yellow]⚠[/yellow] pytest 未安装，跳过测试")

    console.print("[bold]步骤 2/5: 运行 lint...[/bold]")
    try:
        result = subprocess.run(
            ["ruff", "check", "."],
            capture_output=True, text=True, cwd=str(PROJECT_ROOT),
            timeout=30,
        )
        if result.returncode != 0:
            console.print("[red]Lint 未通过，停止同步[/red]")
            console.print(result.stdout[-500:] if result.stdout else "")
            return 1
        console.print("  [green]✓[/green] Lint 通过")
    except FileNotFoundError:
        console.print("[yellow]⚠[/yellow] ruff 未安装，跳过 lint")

    # 2. 检查当前分支
    console.print("[bold]步骤 3/5: 检查分支...[/bold]")
    try:
        result = subprocess.run(
            ["git", "branch", "--show-current"],
            capture_output=True, text=True, cwd=str(PROJECT_ROOT),
        )
        current_branch = result.stdout.strip()

        if not current_branch:
            console.print("[red]无法获取当前分支[/red]")
            return 1

        console.print(f"  当前分支: [cyan]{current_branch}[/cyan]")

        # 禁止直推主干
        if current_branch in ("main", "master"):
            console.print("[red]禁止直推主干！请使用功能分支[/red]")
            return 1
    except Exception as e:
        console.print(f"[red]Git 检查失败: {e}[/red]")
        return 1

    # 3. 检测 origin
    console.print("[bold]步骤 4/5: 检测远程仓库...[/bold]")
    try:
        result = subprocess.run(
            ["git", "remote", "get-url", "origin"],
            capture_output=True, text=True, cwd=str(PROJECT_ROOT),
        )
        if result.returncode != 0:
            console.print("[red]未检测到 origin 远程仓库[/red]")
            console.print("[yellow]请配置 GitHub remote:[/yellow]")
            console.print("  git remote add origin <your-repo-url>")
            return 1
        console.print(f"  origin: [dim]{result.stdout.strip()}[/dim]")
    except Exception as e:
        console.print(f"[red]远程仓库检测失败: {e}[/red]")
        return 1

    # 4. 提交
    console.print("[bold]步骤 5/5: 提交并推送...[/bold]")
    try:
        # 检查是否有变更
        status_result = subprocess.run(
            ["git", "status", "--porcelain"],
            capture_output=True, text=True, cwd=str(PROJECT_ROOT),
        )
        if not status_result.stdout.strip():
            console.print("  [yellow]无变更，跳过提交[/yellow]")
            return 0

        # git add
        subprocess.run(["git", "add", "."], check=True, cwd=str(PROJECT_ROOT))

        # 生成中文 commit message
        commit_msg = f"Phase 完成 — {current_branch}"
        subprocess.run(
            ["git", "commit", "-m", commit_msg],
            check=True, cwd=str(PROJECT_ROOT),
        )
        console.print(f"  [green]✓[/green] 提交: {commit_msg}")

        # git push
        subprocess.run(
            ["git", "push", "-u", "origin", current_branch],
            check=True, cwd=str(PROJECT_ROOT),
        )
        console.print(f"  [green]✓[/green] 推送成功: {current_branch}")

    except subprocess.CalledProcessError as e:
        console.print(f"[red]Git 操作失败: {e}[/red]")
        return 1

    console.print("\n[bold green]Git 同步完成！[/bold green]")
    return 0
