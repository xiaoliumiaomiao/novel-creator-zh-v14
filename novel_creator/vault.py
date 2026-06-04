"""Obsidian vault 管理 — 初始化、模板、样例生成."""

# ruff: noqa: E501  (样本章节含长行中文正文)

from __future__ import annotations

import contextlib
import sys
from pathlib import Path

from rich.console import Console

from novel_creator.config import VAULT_DIR, VAULT_SUBDIRS

if sys.platform == "win32":
    with contextlib.suppress(Exception):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")

console = Console(force_terminal=True)

# 章节模板
CHAPTER_TEMPLATE = """---
type: chapter
book: {book}
track: {track}
status: drafted
chapter_no: {chapter_no}
title: {title}
effective_word_count: 0
english_ratio: 0
commercial_score: 0
continuity_score: 0
deai_score: 0
risk_status: pass
---

# 第{chapter_no}章 {title}

正文第一段。
正文第二段。
"""

# 人物卡模板
CHARACTER_TEMPLATE = """---
type: character
book: {book}
name: {name}
role: {role}
status: active
---

# {name}

## 基本信息

- 姓名：
- 性别：
- 年龄：
- 身份：
- 首次出场：

## 性格

## 外貌

## 背景

## 能力

## 关系

## 动机

## 弧线
"""

# 世界观模板
WORLDBUILDING_TEMPLATE = """---
type: worldbuilding
book: {book}
category: {category}
status: draft
---

# {title}

## 概述

## 规则

## 限制

## 关联人物

## 关联事件
"""

# 章纲模板
PLOT_TEMPLATE = """---
type: plot
book: {book}
level: {level}
status: draft
---

# {title}

## 目标

## 冲突

## 节奏

## 爽点/钩子

## 章纲列表
"""

# 仪表盘模板
DASHBOARD_TEMPLATE = """---
type: dashboard
updated: {date}
---

# 创作仪表盘

## 项目总览

## 章节进度

## 字数统计

## 风险状态

## 评分趋势

## 伏笔状态

## 人物变化

## Agent Trace 索引
"""


def init_vault() -> int:
    """初始化 vault 目录、模板、仪表盘和样例.

    Returns:
        0 成功, 1 失败.
    """
    console.print("[bold cyan]初始化 Obsidian Vault...[/bold cyan]")

    # 创建 vault 根目录和子目录
    for subdir in VAULT_SUBDIRS:
        dir_path = VAULT_DIR / subdir
        dir_path.mkdir(parents=True, exist_ok=True)
        console.print(f"  [green]✓[/green] 创建目录: {dir_path}")

    # 创建 References README
    ref_readme = VAULT_DIR / "References" / "README.md"
    ref_readme.write_text(
        "# References\n\n"
        "参考库 — IMA 和网络参考导入区。\n\n"
        "**此目录内容默认不提交 Git。**\n\n"
        "## 使用规则\n\n"
        "- 只允许学习结构模式（开局、冲突密度、钩子类型、情绪曲线、爽点分布、节奏）\n"
        "- 禁止保存可复用原文\n"
        "- 禁止将参考原文写入 Agent 提示词\n"
        "- 禁止摘录长段正文\n",
        encoding="utf-8",
    )
    console.print("  [green]✓[/green] 创建 References README")

    # 创建模板
    templates_dir = VAULT_DIR / "Templates"
    _write_template(templates_dir / "章节模板.md", CHAPTER_TEMPLATE.format(
        book="book-id", track="male", chapter_no="N", title="标题"
    ))
    _write_template(templates_dir / "人物卡模板.md", CHARACTER_TEMPLATE.format(
        book="book-id", name="角色名", role="主角/配角/反派"
    ))
    _write_template(templates_dir / "世界观模板.md", WORLDBUILDING_TEMPLATE.format(
        book="book-id", category="等级/势力/地理/规则", title="设定名"
    ))
    _write_template(templates_dir / "章纲模板.md", PLOT_TEMPLATE.format(
        book="book-id", level="volume/chapter", title="标题"
    ))
    console.print("  [green]✓[/green] 创建模板文件")

    # 创建仪表盘
    from datetime import date

    dashboard_dir = VAULT_DIR / "00_Dashboard"
    dashboard_md = dashboard_dir / "Dashboard.md"
    dashboard_md.write_text(
        DASHBOARD_TEMPLATE.format(date=date.today().isoformat()),
        encoding="utf-8",
    )
    console.print("  [green]✓[/green] 创建仪表盘")

    # 创建迷你样例
    _create_samples()
    console.print("  [green]✓[/green] 创建迷你样例")

    console.print("\n[bold green]Vault 初始化完成！[/bold green]")
    console.print(f"  用 Obsidian 打开: [bold]{VAULT_DIR}[/bold]")
    return 0


def _write_template(path: Path, content: str) -> None:
    """写入模板文件."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def _create_samples() -> None:
    """创建男频/女频迷你样例."""
    samples_dir = VAULT_DIR / "Samples"

    # 男频迷你样例
    male_dir = samples_dir / "sample-male"
    male_dir.mkdir(parents=True, exist_ok=True)

    male_chapter = male_dir / "第1章 初入局中.md"
    male_chapter.write_text(
        """---
type: chapter
book: sample-male
track: male
status: drafted
chapter_no: 1
title: 初入局中
effective_word_count: 825
english_ratio: 0
commercial_score: 86
continuity_score: 88
deai_score: 87
risk_status: pass
---

# 第1章 初入局中

林北睁开眼，头顶是陌生的天花板。

这是他穿越到玄灵大陆的第三天。空气里飘着一股灵草的清香，和前世北京的雾霾完全不是一回事。

“林北，还睡？测灵根要迟到了！”

门被一脚踢开，一个扎着马尾的少年冲进来，脸上写满了兴奋。

林北坐起来，揉了揉眉心。前身的记忆还在融合——这具身体的主人也叫林北，青阳城外门弟子，灵根资质评定为下等。在宗门里，下等灵根意味着什么？意味着扫地。

但他不在乎。因为穿越的时候，他脑子里多了个东西。

那是一本《玄灵大陆速通攻略》。

准确说，是他在穿越前正在玩的那款修仙游戏的全成就攻略，包含所有隐藏任务、捷径路线和最终 Boss 的战法。而现在，这本攻略就刻在他的识海里，像一本翻不完的金书。

“知道了。”林北套上外袍，跟着少年往外走。

路上他翻了一下攻略里的新手篇。第一条建议就让他心里一喜：

【青阳城测灵台西南角，第三块地砖下埋着一枚洗髓丹，可提升灵根品阶。需在辰时阳气最盛时挖取。】

测灵台。西南角。第三块地砖。

林北嘴角勾起一个弧度。

他不知道谁留下的攻略，也不知道为什么攻略会印在自己脑子里。但他知道一件事：

在别人还在新手村摸索的时候，他已经拿到了通关攻略。

这游戏，他要换个玩法。

测灵台前人山人海。今天是外门弟子年度测评的日子，成绩好的能晋升内门，差的就继续扫地。林北站在队列末尾，眼睛一直盯着西南角。

“林北！”负责测试的执事喊道。

轮到他的时候，他已经把那块地砖的位置记得清清楚楚。

测灵石亮起微弱的光芒——下等灵根，毫无悬念。

周围传来几声嗤笑。

林北没理会，走下台的时候漫不经心地绊了一下，手撑在地上正好按到第三块地砖。指尖碰到一个冰凉的凸起。

他不动声色地将东西收进袖口，转身离开了测灵台。

回到住处，他摊开手掌。一枚暗金色的丹药躺在掌心，散发着微弱的热度。

洗髓丹。

林北一口吞下。

剧痛从骨髓深处涌上来，像每一根骨头都在被敲碎重组。他咬紧牙关，汗如雨下。

半个时辰后，疼痛消退。

他睁开眼，世界变得不一样了——空气中的灵草清香变成了可见的绿色光点，远处测灵台的喧嚣听在耳中清晰得过分。

更关键的是，攻略里的第二页亮了起来：

【灵根已提升至中品。下一目标：青阳城外黑风林深处，有一处废弃洞府，洞府主人遗留功法《天罡诀》，适配中品灵根。】

林北深吸一口气。

青阳城外，黑风林，废弃洞府。

好，下一个副本，出发。
""",
        encoding="utf-8",
    )

    # 女频迷你样例
    female_dir = samples_dir / "sample-female"
    female_dir.mkdir(parents=True, exist_ok=True)

    female_chapter = female_dir / "第1章 重生归来.md"
    female_chapter.write_text(
        """---
type: chapter
book: sample-female
track: female
status: drafted
chapter_no: 1
title: 重生归来
effective_word_count: 885
english_ratio: 0
commercial_score: 88
continuity_score: 90
deai_score: 86
risk_status: pass
---

# 第1章 重生归来

苏晚醒来的时候，嘴里还残留着那杯毒酒的苦味。

她猛地坐起来，手摸上自己的脖子——完整的，没有伤口。眼前是一间古色古香的闺房，窗外的桃花开得正盛。

这是她在永安侯府的闺房。

那是二十年前的样子。

“小姐，您醒了？太子殿下的聘礼已经送到前厅了，夫人让您梳洗后过去。”

丫鬟春桃端着铜盆进来，脸上带着喜气。

太子殿下。聘礼。

苏晚的手指紧紧攥住了被褥。

上一世，就是这桩婚事，把她推进了深渊。太子萧衍娶她不过是为了侯府的兵权，登基之后立刻翻脸，抄了苏家满门。她跪在午门前求了三天，最后等来的是萧衍的一杯毒酒，以及新后——她那个庶妹苏瑶——站在台阶上看着她的笑。

那一天，苏瑶说：“姐姐，你以为他当真喜欢过你吗？”

喉间的烧灼感还没退去，苏晚闭了闭眼。

再睁开时，眼眶已经不红了。

既然老天给了她重来一次的机会，这一次，她不会再做任人拿捏的软柿子。

“春桃，把那套大红色的裙子拿来。”苏晚掀开被子，声音平静。

“小姐？那套不是您说太艳了——”

“我说拿来。”

苏晚的语气没有起伏，但春桃莫名觉得今天的小姐和往常不一样。她也说不清哪里不一样，只是觉得小姐看人的眼神，像是把什么都看透了。

梳妆台上，铜镜映出一张十六岁的脸。

苏晚伸手摸了摸那张还带着稚气的面容。二十年的恩怨生死，都装在这张年轻的皮囊里。

前厅，太子萧衍正坐在太师椅上，姿态矜贵。他今日穿了件月白色的锦袍，衬得面容如玉，一双含笑的眼睛朝她看过来。

苏晚进门的时候，萧衍站了起来，温声道：“苏大小姐，一别三月，可还安好？”

上一世，苏晚就是被这副温柔的表象骗了。

她屈膝行了个礼，抬起眼的时候，眼底没有半点波澜。

“承蒙殿下挂念，臣女一切安好。”

萧衍微微一愣。他说不上哪里不对，但面前这个少女看他的目光，没有了上次相见时的羞怯。

那目光平静得像在看一个路人。

“聘礼我已让母亲清点入库。”苏晚继续道，声音清脆，“不过有件事，想请殿下赐教。”

“你说。”

“陛下的赐婚圣旨上写的是‘苏氏嫡女’。殿下可否确认，圣旨上指的是哪位苏氏嫡女？”

萧衍的笑容淡了。

“侯爷只有你一个嫡女，自是——”

“既是如此，为何京城盛传殿下与舍妹苏瑶两情相悦？”苏晚微微一笑，“此事若传到陛下耳中，恐有欺君之嫌。”

前厅安静了一瞬。

萧衍盯着她看了片刻，忽然笑了：“苏大小姐今日似乎与往常不同。”

“大概是昨夜没睡好，脑子清醒了些。”苏晚垂下眼睫，“殿下若无其他吩咐，臣女告退。”

她转身走出去的时候，后背挺得笔直。

二十年前她选了忍让，选了委屈求全。

这一次，她不争不抢——她要让这些人亲手把欠她的，一寸寸还回来。
""",
        encoding="utf-8",
    )
    console.print("    [green]✓[/green] sample-male/第1章 初入局中.md")
    console.print("    [green]✓[/green] sample-female/第1章 重生归来.md")


def ensure_vault_exists() -> bool:
    """检查 vault 是否已初始化."""
    return VAULT_DIR.exists() and (VAULT_DIR / "00_Dashboard").exists()
