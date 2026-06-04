"""novelctl CLI 入口 — 中文网文工业化创作工具集.

用法:
    novelctl --help
    novelctl init-vault
    novelctl lint
    novelctl dashboard
    ...
"""

from __future__ import annotations

import contextlib
import sys
from pathlib import Path

from rich.console import Console

# 确保 Windows 终端使用 UTF-8 编码
if sys.platform == "win32":
    with contextlib.suppress(Exception):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")

console = Console(force_terminal=True)


def _cmd_init_vault() -> int:
    """初始化 Obsidian vault 目录结构、模板、仪表盘和样例."""
    from novel_creator.vault import init_vault

    return init_vault()


def _cmd_import_ima(source: str | None = None) -> int:
    """从 vault/References 导入并分析 IMA Markdown 文件."""
    from novel_creator.corpus import import_ima

    source_path = Path(source) if source else None
    return import_ima(source_path)


def _cmd_index() -> int:
    """构建本地 SQLite 索引."""
    from novel_creator.corpus import build_index

    return build_index()


def _cmd_extract_patterns() -> int:
    """提炼写作结构模式."""
    from novel_creator.corpus import extract_patterns

    return extract_patterns()


def _cmd_score_chapter(file: str) -> int:
    """对章节进行多维度评分."""
    from novel_creator.scoring import score_chapter

    return score_chapter(Path(file))


def _cmd_deai(file: str, mode: str = "detail-light") -> int:
    """对文件进行去 AI 味处理.

    mode: expression-only | detail-light | dramatic-boost
    """
    from novel_creator.deai import process_deai

    return process_deai(Path(file), mode)


def _cmd_lint() -> int:
    """运行完整硬规则检查."""
    from novel_creator.linting import run_lint

    return run_lint()


def _cmd_dashboard() -> int:
    """生成 Markdown + HTML 仪表盘."""
    from novel_creator.dashboard import generate_dashboard

    return generate_dashboard()


def _cmd_publish_check() -> int:
    """发布前总闸门检查."""
    from novel_creator.linting import run_publish_check

    return run_publish_check()


def _cmd_git_sync() -> int:
    """安全 Git 同步：测试通过后 commit + push 当前功能分支."""
    from novel_creator.git_sync import git_sync

    return git_sync()


def _cmd_trace(project: str | None = None) -> int:
    """查看 Agent Trace 列表和内容."""
    from novel_creator.orchestration import list_traces

    traces = list_traces(project)
    if not traces:
        console.print("[yellow]未找到 Agent Trace[/yellow]")
        return 0

    console.print(f"[bold cyan]找到 {len(traces)} 条 Agent Trace:[/bold cyan]\n")
    for t in traces[:20]:
        size = t.stat().st_size
        console.print(f"  [green]•[/green] {t.name} ([dim]{size} bytes[/dim])")
        # 显示摘要
        content = t.read_text(encoding="utf-8")[:200]
        summary = content.split("\n")[5] if len(content.split("\n")) > 5 else ""
        if summary:
            console.print(f"    [dim]{summary[:80]}...[/dim]")

    return 0


HELP_TEXT = """
novelctl — 中文网文工业化创作工具集 CLI

用法:
    novelctl <command> [options]

命令:
    init-vault          初始化 Obsidian vault 目录结构、模板、仪表盘和样例
    import-ima          从 vault/References 导入分析 IMA Markdown
    index               构建本地 SQLite 索引
    extract-patterns    提炼写作结构模式（开局、冲突密度、钩子类型等）
    score-chapter       对章节进行多维度评分
    deai                去 AI 味处理（三模式）
    lint                运行完整硬规则检查
    dashboard           生成 Markdown + HTML 仪表盘
    publish-check       发布前总闸门检查
    git-sync            安全 Git 同步
    trace               查看 Agent Trace

全局选项:
    --help              显示此帮助信息
    --version           显示版本号
"""


def print_help() -> None:
    """打印帮助信息."""
    console.print(HELP_TEXT, style="bold white")


def print_version() -> None:
    """打印版本号."""
    from novel_creator import __version__

    console.print(f"novelctl v{__version__}", style="bold cyan")


def main() -> int:
    """CLI 主入口."""
    args = sys.argv[1:]

    if not args or "--help" in args or "-h" in args:
        print_help()
        return 0

    if "--version" in args or "-V" in args:
        print_version()
        return 0

    command = args[0]
    cmd_args = args[1:]

    commands: dict[str, callable] = {
        "init-vault": lambda: _cmd_init_vault(),
        "import-ima": lambda: _cmd_import_ima(cmd_args[0] if cmd_args else None),
        "index": lambda: _cmd_index(),
        "extract-patterns": lambda: _cmd_extract_patterns(),
        "score-chapter": lambda: (
            _cmd_score_chapter(cmd_args[0]) if cmd_args else _fail("缺少文件参数")
        ),
        "deai": lambda: _cmd_deai(
            cmd_args[0] if cmd_args else _fail("缺少文件参数"),
            cmd_args[1] if len(cmd_args) > 1 else "detail-light",
        ),
        "lint": lambda: _cmd_lint(),
        "dashboard": lambda: _cmd_dashboard(),
        "publish-check": lambda: _cmd_publish_check(),
        "git-sync": lambda: _cmd_git_sync(),
        "trace": lambda: _cmd_trace(cmd_args[0] if cmd_args else None),
    }

    if command not in commands:
        console.print(f"[red]未知命令: {command}[/red]")
        console.print("运行 [bold]novelctl --help[/bold] 查看可用命令")
        return 1

    try:
        return commands[command]()
    except Exception as e:
        console.print(f"[red]错误: {e}[/red]")
        return 1


def _fail(msg: str) -> int:
    """打印错误并返回非零码."""
    console.print(f"[red]{msg}[/red]")
    return 1


if __name__ == "__main__":
    sys.exit(main())
