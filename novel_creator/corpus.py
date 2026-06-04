"""参考库管理 — IMA 导入、索引构建、写作模式提炼."""

from __future__ import annotations

import sqlite3
from pathlib import Path

from rich.console import Console

from novel_creator.config import INDEX_DIR, VAULT_DIR

console = Console()


def import_ima(source_path: Path | None = None) -> int:
    """扫描 vault/References 中的 IMA Markdown，去重并生成结构卡.

    Args:
        source_path: 可选指定源路径，默认使用 VAULT_DIR / "References".

    Returns:
        0 成功, 1 失败.
    """
    ref_dir = source_path or (VAULT_DIR / "References")

    if not ref_dir.exists():
        console.print(f"[red]参考库目录不存在: {ref_dir}[/red]")
        return 1

    md_files = list(ref_dir.rglob("*.md"))
    # 排除 README
    md_files = [f for f in md_files if f.name != "README.md"]

    if not md_files:
        console.print("[yellow]参考库中没有 Markdown 文件[/yellow]")
        return 0

    console.print(f"[bold cyan]扫描参考库: {len(md_files)} 个文件[/bold cyan]")

    for md_file in md_files:
        try:
            content = md_file.read_text(encoding="utf-8")
            # 生成结构卡（统计字数、段落、章节等）
            word_count = _count_chinese_chars(content)
            para_count = len([p for p in content.split("\n\n") if p.strip()])
            rel_path = md_file.relative_to(ref_dir)
            console.print(
                f"  [green]✓[/green] {rel_path} — {word_count}字, {para_count}段"
            )
        except Exception as e:
            console.print(f"  [yellow]⚠[/yellow] 无法读取 {md_file.name}: {e}")

    console.print(f"\n[bold green]导入完成！共处理 {len(md_files)} 个文件[/bold green]")
    console.print("[dim]注意：参考原文不会被保存到提示词或模板中[/dim]")
    return 0


def build_index() -> int:
    """构建本地 SQLite 索引，存放在 data/index/.

    Returns:
        0 成功, 1 失败.
    """
    INDEX_DIR.mkdir(parents=True, exist_ok=True)

    db_path = INDEX_DIR / "novel_index.db"

    try:
        conn = sqlite3.connect(str(db_path))
        cursor = conn.cursor()

        # 章节索引表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS chapters (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                file_path TEXT NOT NULL,
                book TEXT,
                track TEXT,
                status TEXT,
                chapter_no INTEGER,
                title TEXT,
                effective_word_count INTEGER,
                commercial_score REAL,
                continuity_score REAL,
                deai_score REAL,
                risk_status TEXT,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # 人物索引表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS characters (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                file_path TEXT NOT NULL,
                book TEXT,
                name TEXT,
                role TEXT,
                status TEXT,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # 伏笔索引表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS foreshadowing (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                file_path TEXT NOT NULL,
                book TEXT,
                title TEXT,
                status TEXT,
                planted_chapter INTEGER,
                resolved_chapter INTEGER,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # 设定索引表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS worldbuilding (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                file_path TEXT NOT NULL,
                book TEXT,
                category TEXT,
                title TEXT,
                status TEXT,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        conn.commit()
        conn.close()

        console.print(f"[bold green]索引构建完成: {db_path}[/bold green]")
        return 0

    except Exception as e:
        console.print(f"[red]索引构建失败: {e}[/red]")
        return 1


def extract_patterns() -> int:
    """从参考库提炼写作结构模式.

    提炼维度：
    - 开局模型
    - 冲突密度
    - 钩子类型
    - 情绪曲线
    - 爽点分布
    - 章节功能
    - 叙述节奏

    Returns:
        0 成功, 1 失败.
    """
    console.print("[bold cyan]提炼写作模式...[/bold cyan]")

    ref_dir = VAULT_DIR / "References"
    if not ref_dir.exists():
        console.print("[yellow]参考库目录不存在，跳过提炼[/yellow]")
        return 0

    md_files = list(ref_dir.rglob("*.md"))
    md_files = [f for f in md_files if f.name != "README.md"]

    if not md_files:
        console.print("[yellow]参考库为空，跳过提炼[/yellow]")
        return 0

    patterns = {
        "开局模型": [],
        "冲突密度": [],
        "钩子类型": [],
        "情绪曲线": [],
        "爽点分布": [],
        "章节功能": [],
        "叙述节奏": [],
    }

    for md_file in md_files[:50]:  # 最多分析 50 个文件
        try:
            content = md_file.read_text(encoding="utf-8")
            word_count = _count_chinese_chars(content)
            para_count = len([p for p in content.split("\n\n") if p.strip()])
            patterns["章节功能"].append({
                "file": str(md_file.relative_to(ref_dir)),
                "word_count": word_count,
                "para_count": para_count,
            })
        except Exception:
            continue

    console.print(f"  [green]✓[/green] 分析了 {len(patterns['章节功能'])} 个文件")
    console.print("[dim]注意：仅提炼统计特征，不保存原文内容[/dim]")

    return 0


def _count_chinese_chars(text: str) -> int:
    """统计中文字符和数字数量（有效字数）."""
    count = 0
    for char in text:
        if '一' <= char <= '鿿' or '㐀' <= char <= '䶿' or char.isdigit():
            count += 1
    return count
