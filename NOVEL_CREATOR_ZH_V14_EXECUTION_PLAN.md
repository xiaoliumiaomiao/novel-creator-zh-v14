# Novel Creator ZH V14.0 Execution Plan

> 本文件用于交给挂载 DeepSeekV4Pro API 的 Claude Code 执行。  
> 你不是在讨论方案，而是在按本计划搭建一个可运行、可验收、可提交 GitHub 的中文网文工业化创作工具集。

## DeepSeekV4Pro Claude Code Execution Config

### 执行身份

你是执行工程师，不是方案顾问。必须按本文档完成搭建，不得擅自改变产品方向、目录结构、核心规则和验收标准。

### 总执行原则

1. 必须按 Phase 顺序执行，不得跳阶段。
2. 每次只执行一个 Phase。
3. 每个 Phase 开始前，先阅读对应主计划章节和附录规则。
4. 每个 Phase 开始时，列出本阶段将创建或修改的文件清单。
5. 核心文件必须写实，禁止空壳、伪实现、占位式 TODO。
6. 非核心演示内容可少量 TODO，但不得影响主流程运行。
7. 每个 Phase 完成后，必须运行本阶段验收命令。
8. 验收失败时必须修复，最多自动修复 2 轮。
9. 修复 2 轮后仍失败，必须停止并报告，不得继续下一阶段。
10. 验收通过后，输出阶段验收表。
11. 验收通过后再 commit + push 当前功能分支。

### 禁止事项

- 禁止单个 Agent 包办小说创作工作流。
- 禁止跳过创作期多 Agent 编排。
- 禁止跳过 Agent Trace。
- 禁止提交 `vault/References/**` 中的参考原文。
- 禁止把参考库原文写进提示词、模板或生成素材库。
- 禁止自动直推主干。
- 禁止测试失败后假装完成。
- 禁止用空文件冒充已完成 Agent、Skill、CLI、测试或文档。
- 禁止把本工具做成单纯提示词合集；必须有可运行 Python CLI、测试和仪表盘。

### Git 执行规则

1. 默认使用功能分支，禁止自动直推 `main` 或 `master`。
2. 如果当前不在功能分支，创建或切换到 `codex/novel-creator-zh-v14`。
3. 每阶段验收通过后提交。
4. Commit message 使用中文摘要，例如：`新增 V14 小说创作工具集基础工程`。
5. 检测已有 `origin` 后再 push。
6. 如果没有 `origin`，停止 push 并提示用户配置 GitHub remote。
7. GitHub 仓库默认私有。

### 阶段验收表模板

每个 Phase 完成后输出：

```markdown
## Phase N 验收表

- 阶段名称：
- 完成文件：
- 运行命令：
- 通过项：
- 失败项：
- 自动修复次数：
- 剩余风险：
- Git commit：
- Git push：
- 下一阶段建议：
```

---

## 1. Project Summary

### 目标

从空目录搭建 `novel-creator-zh-v14.0`：一套中文网文工业化创作工具集，供 Claude Code 在实际创作小说时调用多个专职 Agent 协作完成立项、设定、大纲、章节、正文、审稿、去 AI 味、修订、复盘和发布前检查。

### 产品形态

- Claude Code 项目内工具集。
- Obsidian vault 知识中枢。
- Python CLI 程序。
- Markdown + HTML 仪表盘。
- GitHub 私有仓库自动提交与推送流程。
- GitHub Actions 完整 CI。

### 创作定位

- 中文网文。
- 番茄/七猫口味优先。
- 男频/女频完全双套。
- 支持人主导模式和高自动批量模式。
- 高自动批量模式每章后必须停下审阅。

### 核心要求

- 创作期必须自动调用多个专职 Agent。
- 不能由一个 Agent 把所有活干完。
- 必须保留详细 Agent Trace。
- 每章生成后必须更新人物、伏笔、时间线和设定库的待确认记忆。
- 必须内置去 AI 味工具。
- 必须内置法律、政治、平台风险审查。
- 必须内置章节硬规则检查。

主计划中的细节规则集中在以下附录：

- [Appendix A: Writing Hard Rules](#appendix-a-writing-hard-rules)
- [Appendix B: Style Blacklist](#appendix-b-style-blacklist)
- [Appendix C: Risk Review Rules](#appendix-c-risk-review-rules)
- [Appendix D: Agent Orchestration Contract](#appendix-d-agent-orchestration-contract)
- [Appendix E: Git And CI Rules](#appendix-e-git-and-ci-rules)
- [Appendix F: Acceptance Checklist](#appendix-f-acceptance-checklist)

---

## 2. Required Repository Structure

执行端必须创建以下结构。

```text
.
├── README.md
├── CLAUDE.md
├── NOVEL_CREATOR_ZH_V14_EXECUTION_PLAN.md
├── pyproject.toml
├── .gitignore
├── .github/
│   └── workflows/
│       └── ci.yml
├── .claude/
│   ├── agents/
│   ├── skills/
│   └── commands/
├── novel_creator/
│   ├── __init__.py
│   ├── cli.py
│   ├── vault.py
│   ├── corpus.py
│   ├── scoring.py
│   ├── dashboard.py
│   ├── linting.py
│   ├── git_sync.py
│   ├── deai.py
│   ├── risk.py
│   ├── orchestration.py
│   └── config.py
├── scripts/
│   ├── check.ps1
│   ├── check.py
│   └── git_sync.py
├── tests/
│   ├── test_vault.py
│   ├── test_linting.py
│   ├── test_scoring.py
│   ├── test_deai.py
│   ├── test_risk.py
│   ├── test_orchestration.py
│   └── test_cli_smoke.py
├── reports/
├── data/
│   └── index/
└── vault/
    ├── 00_Dashboard/
    │   └── Agent_Traces/
    ├── 01_Projects/
    ├── 02_Characters/
    ├── 03_Worldbuilding/
    ├── 04_Plot/
    ├── 05_Chapters/
    ├── 06_Foreshadowing/
    ├── 07_Timeline/
    ├── References/
    ├── Templates/
    └── Samples/
```

---

## 3. Root Files

### `README.md`

必须包含：

- 产品简介。
- 安装方式。
- 快速开始。
- Obsidian 插件建议。
- Claude Code 使用方式。
- CLI 使用方式。
- GitHub 推送规则。
- 参考库版权与隐私边界。

### `CLAUDE.md`

必须包含：

- 本项目是中文网文工业化创作工具集。
- Claude Code 在创作期必须使用多 Agent。
- 所有章节必须通过硬规则检查。
- 所有章节必须通过风险检查。
- 所有章节进入 `approved` 前必须用户确认。
- 禁止提交参考库原文。
- 禁止单 Agent 包办整条创作链路。
- 触犯已有硬规则时自动回修；没有规则覆盖的问题报告用户决定。

### `pyproject.toml`

必须配置：

- 包名：`novel-creator-zh`
- Python 版本：`>=3.10`
- CLI 入口：`novelctl = "novel_creator.cli:main"`
- 依赖：`PyYAML`、`rich`
- 开发依赖：`pytest`、`ruff`、`build`
- ruff 基础配置。
- pytest 基础配置。

### `.gitignore`

必须忽略：

```gitignore
__pycache__/
.pytest_cache/
.ruff_cache/
.mypy_cache/
dist/
build/
*.egg-info/
data/index/*.db
data/index/*.sqlite
reports/*.tmp
vault/.obsidian/workspace*
vault/.trash/
vault/References/**
!vault/References/README.md
```

---

## 4. Obsidian Vault Design

`vault/` 是 Obsidian vault，也是小说项目知识中枢。

### 推荐 Obsidian 插件

官方 Core 插件作为底座：

- Bases
- Properties view
- Graph view
- Canvas
- Backlinks
- Templates
- Word count

社区插件作为稳健增强：

- Longform：可选编排，不承担核心流程。
- Ima Vault：用于腾讯 ima 导入。
- Dataview：只读可选，禁止 DataviewJS 进入核心流程。

### Vault 目录说明

- `00_Dashboard/`：总览、进度、仪表盘、Agent Trace。
- `01_Projects/`：每本书的主项目文档。
- `02_Characters/`：人物卡。
- `03_Worldbuilding/`：世界观、等级、势力、规则。
- `04_Plot/`：主线、卷纲、章纲。
- `05_Chapters/`：章节正文和版本。
- `06_Foreshadowing/`：伏笔新增、回收、悬而未决项。
- `07_Timeline/`：时间线。
- `References/`：ima 和网络参考导入区，默认不提交 Git。
- `Templates/`：模板。
- `Samples/`：男频/女频迷你双样例。

---

## 5. Markdown And YAML Data Model

所有正文、设定、人物、大纲文件用 Markdown。需要工具识别的文件必须带 YAML properties。

章节文件示例：

```markdown
---
type: chapter
book: sample-male
track: male
status: drafted
chapter_no: 1
title: 初入局中
effective_word_count: 3120
english_ratio: 0
commercial_score: 86
continuity_score: 88
deai_score: 87
risk_status: pass
---

# 第1章 初入局中

正文第一段。
正文第二段。
```

状态流：

```text
planned -> drafted -> reviewed -> deai -> polished -> approved
```

打回支线：

```text
rejected -> revision-planned -> revised -> reviewed
```

被打回稿命名：

```text
第1章 标题.v02-rejected.md
```

---

## 6. Python CLI Requirements

CLI 名称：`novelctl`

必须实现命令：

```text
novelctl init-vault
novelctl import-ima --source vault/References
novelctl index
novelctl extract-patterns
novelctl score-chapter <chapter.md>
novelctl deai <file.md> --mode detail-light
novelctl lint
novelctl dashboard
novelctl publish-check
novelctl git-sync
```

### `novelctl init-vault`

必须：

- 创建 vault 目录。
- 创建模板。
- 创建仪表盘。
- 创建男频/女频迷你样例。
- 创建 `vault/References/README.md`。

### `novelctl import-ima`

必须：

- 扫描 `vault/References`。
- 读取 Markdown。
- 去重。
- 生成结构卡。
- 不保存可复用原文到提示词或模板。

### `novelctl index`

必须：

- 建立本地 SQLite 索引。
- 索引文件放在 `data/index/`。
- 索引文件不提交 Git。

### `novelctl extract-patterns`

必须提炼：

- 开局模型。
- 冲突密度。
- 钩子类型。
- 情绪曲线。
- 爽点分布。
- 章节功能。
- 叙述节奏。

### `novelctl score-chapter`

必须输出：

- 商业节奏评分。
- 连续性评分。
- 人物动机评分。
- 去 AI 味评分。
- 风险状态。
- 字数和格式检查结果。

### `novelctl deai`

必须：

- 支持 `expression-only`、`detail-light`、`dramatic-boost`。
- 输出三稿并存：`original`、`natural`、`web-serial`。
- 不破坏商业节奏。
- 不新增重大剧情事实。
- `dramatic-boost` 如新增小反应或小冲突，必须标注新增处。

### `novelctl lint`

必须检查：

- YAML properties。
- Obsidian 双链。
- 章节状态。
- 有效字数。
- 空行。
- 英文比例。
- 段落长度。
- 中文标点。
- 禁用句式。
- 参考库 Git 保护。
- 法律/政治风险。

### `novelctl publish-check`

必须作为发布前总闸门，检查：

- 正文规则。
- 风险规则。
- 字数规则。
- 空行规则。
- 英文比例。
- 段落长度。
- YAML。
- 链接。
- 状态。
- Agent Trace。
- 参考库泄漏。

### `novelctl git-sync`

必须：

- 先运行测试和 lint。
- 检测 Git。
- 检测当前分支。
- 禁止直推主干。
- 检测 `origin`。
- 使用中文 commit message。
- push 当前功能分支。

---

## 7. Claude Agents

Agent 文件放在 `.claude/agents/`。

每个 Agent 文件必须包含：

- 职责。
- 禁止事项。
- 输入。
- 输出。
- 工作步骤。
- 检查清单。
- 与其他 Agent 的交接方式。

### 男频 Agent

必须创建：

- `male-director.md`
- `male-market-architect.md`
- `male-worldbuilder.md`
- `male-character-architect.md`
- `male-plot-architect.md`
- `male-chapter-planner.md`
- `male-drafter.md`
- `male-commercial-reviewer.md`
- `male-continuity-auditor.md`
- `male-polisher.md`

男频重点：

- 爽点。
- 冲突。
- 升级。
- 目标推进。
- 期待感。
- 留存。
- 番茄/七猫阅读门槛。

### 女频 Agent

必须创建：

- `female-director.md`
- `female-market-architect.md`
- `female-worldbuilder.md`
- `female-character-architect.md`
- `female-plot-architect.md`
- `female-chapter-planner.md`
- `female-drafter.md`
- `female-commercial-reviewer.md`
- `female-continuity-auditor.md`
- `female-polisher.md`

女频重点：

- 人设吸引力。
- 关系递进。
- 情绪钩子。
- 情感爽点。
- 身份张力。
- 女性向读者期待。

### 共享 Agent

必须创建：

- `obsidian-librarian.md`
- `corpus-analyst.md`
- `program-operator.md`
- `anti-ai-voice-editor.md`

---

## 8. Claude Skills And Commands

Skill 文件放在 `.claude/skills/<name>/SKILL.md`。

必须创建：

- `novel-init`
- `male-start`
- `female-start`
- `male-chapter`
- `female-chapter`
- `male-batch`
- `female-batch`
- `novel-audit`
- `novel-import-ima`
- `novel-score`
- `novel-status`
- `novel-deai`

每个 Skill 必须包含：

- 用途。
- 使用场景。
- 输入格式。
- 多 Agent 调用顺序。
- 输出文件。
- 自动检查。
- 失败处理。
- Agent Trace 要求。

如果执行端 Claude Code 不支持 `.claude/skills` slash workflow，则必须同步生成 `.claude/commands/*.md` 作为降级入口。

---

## 9. Runtime Multi-Agent Orchestration

这是工具投入创作使用时的运行规则，不是搭建项目时的执行方式。

默认模式：导演编排。

### 章节创作最小 Agent 链

每次 `/male-chapter` 或 `/female-chapter` 至少调用：

1. Director
2. Plot/Chapter Planner
3. Character Agent
4. Drafter
5. Commercial Reviewer
6. Continuity Auditor
7. Anti-AI Voice Editor
8. Polisher
9. Obsidian Librarian

禁止单个 Agent 从章纲到终稿全部包办。

### Director 职责

Director 必须：

- 读取项目记忆。
- 读取当前章纲。
- 读取最近三章。
- 拆解任务。
- 调度 Agent。
- 汇总冲突。
- 按优先级裁决。
- 输出最终交付包。

裁决优先级：

```text
商业节奏 > 法律/政治风险 > 设定一致性 > 人物动机 > 去 AI 味 > 文风精修
```

### Agent Trace

每章必须生成详细 Agent Trace。

路径：

```text
vault/00_Dashboard/Agent_Traces/
```

每份 Trace 必须记录：

- 调用时间。
- 项目名。
- 章节号。
- 调用 Agent 列表。
- 每个 Agent 的输入摘要。
- 每个 Agent 的输出摘要。
- 采纳建议。
- 拒绝建议。
- Director 裁决。
- 退回与修复记录。
- 待用户确认事项。

---

## 10. Chapter Workflow

### 输入模式

支持两种：

1. 人主导模式：用户给详细章纲。
2. 高自动模式：用户一句目标即可启动。

### 续写上下文

默认读取：

- 项目记忆。
- 当前章纲。
- 最近三章正文。
- 人物卡。
- 伏笔表。
- 时间线。
- 设定库。

### 用户确认点

中间流程自动完成。最终稿前必须提交：

- 原稿。
- 自然去 AI 味版。
- 强网感版。
- 商业审稿报告。
- 连续性审查报告。
- 法律/政治风险报告。
- Agent Trace。
- 待确认记忆更新。

进入 `approved` 前必须用户确认。

### 返工机制

触犯已有硬规则时自动回修。没有规则覆盖的问题报告用户决定。

自动返修上限：2 轮。

低于 85 分不通过。

---

## 11. Anti-AI Voice System

独立 Skill：`/novel-deai`

独立 Agent：`anti-ai-voice-editor`

### 目标

- 读感自然。
- 网文人味。
- 不以规避 AI 检测为产品目标。
- 保留商业节奏。

### 处理范围

- 正文。
- 简介。
- 设定。
- 人物卡。
- 大纲。
- 审稿稿。
- 全库文本。

### 输出

三稿并存：

```text
original
natural
web-serial
```

### 改写模式

- `expression-only`：只改表达，不新增信息。
- `detail-light`：补动作、感官、心理毛刺、小反应，不新增重大剧情事实。
- `dramatic-boost`：增强小冲突、小反应、段落钩子，必须标注新增处。

### 评分

双评分：

- 清单评分：模板句、解释腔、总结腔、平均句长、情绪毛刺、角色口吻、信息密度。
- 读者视角：是否像自然网文作者表达，是否保留连载吸引力。

---

## 12. Reference And IMA Integration

ima 导入位置：

```text
vault/References/
```

默认不提交 Git。

只允许学习：

- 开局模型。
- 冲突密度。
- 钩子类型。
- 情绪曲线。
- 爽点分布。
- 章节功能。
- 叙述节奏。
- 高层题材模式。

允许：

- 分析腾讯 ima 导入到 Obsidian 的本地 Markdown。
- 分析网络公开高层资料。
- 分析公开试读章节的结构节奏。

禁止：

- 保存可复用原文。
- 摘录长段正文。
- 仿写具体段落。
- 将参考原文写入 Agent 提示词。
- 将参考原文提交 Git。

---

## 13. Genre Presets

题材模板先从 `vault/References` 提炼，缺失题材再联网补高层资料和公开试读结构分析。

题材模板是强参考，不是硬套路。

### 男频首批

- 玄幻
- 都市
- 脑洞
- 悬疑
- 历史
- 科幻
- 游戏
- 修仙

### 女频首批

- 现言
- 古言
- 重生
- 甜宠
- 虐恋
- 年代
- 悬疑
- 幻想

---

## 14. New Book Planning Outputs

`male-start` 和 `female-start` 必须生成完整书籍圣经。

书籍圣经必须包含：

- 书名。
- 简介。
- 核心卖点。
- 目标读者。
- 平台口味。
- 主线。
- 主角。
- 重要配角。
- 反派或阻力系统。
- 世界观。
- 规则和限制。
- 分卷规划。
- 前 30 章精纲。
- 风险边界。
- 禁写内容。
- 商业节奏策略。

默认大纲深度：

```text
卷纲 + 前 30 章精纲
```

---

## 15. Risk Review

默认：平台安全优先。

触发风险时：

1. 自动降险一次。
2. 重新审查。
3. 仍有风险则不予通过。
4. 输出位置、原因、建议。

风险审查必须进入：

- `novelctl lint`
- `novelctl publish-check`
- Commercial Reviewer
- Director 最终裁决

尺度边界：类型适配，但不越过平台硬线。

参考官方规范：

- 网络信息内容生态治理规定：https://www.gov.cn/zhengce/zhengceku/2020-11/25/content_5564110.htm
- 网络出版服务管理规定：https://www.nppa.gov.cn/xxgk/fdzdgknr/zcfg_210/bmgz_213/202112/t20211209_442163.html
- 网络暴力信息治理规定：https://www.cac.gov.cn/2024-06/14/c_1720043894161555.htm

---

## 16. Dashboard And Reports

必须生成 Markdown + HTML 仪表盘。

Markdown 仪表盘放在：

```text
vault/00_Dashboard/
```

HTML 报表放在：

```text
reports/
```

仪表盘至少包含：

- 项目总览。
- 章节状态。
- 字数统计。
- 风险状态。
- 商业评分。
- 去 AI 味评分。
- 伏笔状态。
- 人物变化。
- 时间线更新。
- Agent Trace 链接。
- 参考库结构卡统计。

---

## 17. Quality Gates

章节质量通过阈值：85 分。

自动返修上限：2 轮。

评分优先级：

```text
商业节奏 > 设定一致性 > 人物动机 > 去 AI 味 > 文风精修
```

硬规则不通过时，章节不得进入 `approved`。

---

## 18. Phased Execution

### Phase 1: 基础工程

创建：

- 根目录文件。
- Python 包骨架。
- CLI 入口。
- 测试骨架。
- `.gitignore`。
- GitHub Actions 初版。

验收：

```powershell
python -m pytest
python -m novel_creator.cli --help
```

### Phase 2: Obsidian Vault

创建：

- vault 目录。
- 模板。
- 仪表盘。
- 迷你男频样例。
- 迷你女频样例。
- References README。

验收：

```powershell
novelctl init-vault
novelctl lint
```

### Phase 3: Python CLI 核心

实现：

- Markdown/YAML 解析。
- Obsidian 双链扫描。
- 参考库导入。
- SQLite 索引。
- 评分。
- 报表。
- Git 同步。

验收：

```powershell
python -m pytest
novelctl dashboard
novelctl score-chapter vault/Samples/sample-male/第1章*.md
```

### Phase 4: Agents And Skills

创建：

- 男频完整 Agent。
- 女频完整 Agent。
- 共享 Agent。
- 全部 Skills。
- Commands 降级入口。

验收：

- 每个 Agent 有职责、输入、输出、步骤、检查清单。
- 每个 Skill 有多 Agent 调用顺序。
- `/male-chapter` 和 `/female-chapter` 明确禁止单 Agent 包办。

### Phase 5: Multi-Agent Orchestration And Trace

实现：

- orchestration 合同。
- Trace 模板。
- Trace 生成工具。
- 章节工作流中的多 Agent 记录。

验收：

```powershell
python -m pytest tests/test_orchestration.py
novelctl lint
```

### Phase 6: Reference Corpus And Genre Presets

实现：

- ima Markdown 扫描。
- 结构卡生成。
- 题材预设。
- 参考库保护。

验收：

```powershell
novelctl import-ima --source vault/References
novelctl extract-patterns
python -m pytest tests/test_vault.py tests/test_linting.py
```

### Phase 7: Anti-AI Voice System

实现：

- `anti-ai-voice-editor`
- `/novel-deai`
- `novelctl deai`
- 三稿输出。
- 去 AI 味评分。
- 禁用句式库。

验收：

```powershell
novelctl deai vault/Samples/sample-male/第1章*.md --mode detail-light
python -m pytest tests/test_deai.py
```

### Phase 8: Risk, Publish Check, CI, GitHub

实现：

- 风险审查。
- `publish-check`。
- 完整 CI。
- Git 同步。

验收：

```powershell
novelctl publish-check
python -m pytest
ruff check .
python -m build
novelctl git-sync
```

---

## Appendix A: Writing Hard Rules

这些规则必须可测试，必须进入 `novelctl lint` 和 `novelctl publish-check`。

### 章节长度

- 每章正文有效字数：2500 到 4000。
- 不计空格、换行、标点、符号。
- 中文和数字计入有效字数。
- 正文原则上不出现英文。
- 如特殊词必须使用，英文字符占有效字符比例不得超过 1%。

### 空行

- 小说正文不得出现完全空行。
- 属性区、README、模板、设定文档允许空行。

### 标题和文件名

- 章节标题格式：`第1章 标题`
- 正文文件名格式：`第1章 标题.md`

### 段落

- 单段有效字数上限：180。
- 超限自动按语义拆段。
- 不使用场景分隔符。
- 不使用 `***`。
- 不使用场景小标题，除非用户明确要求。

### 对白

- 使用中文引号：`“……”`
- 说话人单独成段。
- 转述不用引号。

### 标点

- 使用中文标点。
- 少用连续感叹号。
- 少用连续省略号。
- 不使用英文半角标点作为正文常规标点。

### 前三章

- 禁止水文。
- 快速进入主冲突。
- 展示题材卖点。
- 禁止大段设定解释。
- 禁止重复心理。
- 禁止无效寒暄。
- 禁止机械总结。

### 第四章以后

- 水文控制进入审稿检查。
- 允许因情节状态适度调整，但必须由 Commercial Reviewer 给出理由。

### 叙事视角

- 默认第三人称有限视角。
- 单章内少量允许切换视角，但必须清晰、必要、不过度。

---

## Appendix B: Style Blacklist

建立可扩展禁用句式库，供 Agent、lint、deai、publish-check 使用。

### 首批禁用句式

禁止 `A——不是B` 式模板句。

示例：

```text
他抖了一下——不是冷，是灵石在动。
```

禁止原因：

- 读感幼稚。
- AI 腔重。
- 转折机械。
- 容易让读者觉得作者很傻。

### 其他禁用倾向

- 过度解释腔。
- 机械总结腔。
- 模板化金句。
- 尬转折。
- 机械排比。
- 空泛情绪词堆叠。
- 无信息量环境描写。
- 用旁白替代行动。
- 用总结替代冲突。

### 处理方式

- 触发明确禁用句式时自动回修。
- 触发疑似 AI 腔时进入 `/novel-deai` 建议。
- 未覆盖的新问题写入报告，让用户决定是否加入禁用句式库。

---

## Appendix C: Risk Review Rules

默认平台安全优先，宁可误杀。

### 必查风险

- 法律风险。
- 政治风险。
- 涉黄风险。
- 赌博风险。
- 毒品风险。
- 暴恐风险。
- 教唆犯罪。
- 侵权。
- 诽谤。
- 隐私泄露。
- 极端血腥虐杀快感。
- 网络暴力引导。

### 处理流程

1. 标出位置。
2. 标出风险类型。
3. 说明原因。
4. 自动降险一次。
5. 复查。
6. 仍有风险则不通过。
7. 输出建议改法。

### 输出格式

```markdown
## 风险报告

- 通过状态：
- 风险位置：
- 风险类型：
- 原因：
- 已尝试降险：
- 复查结果：
- 建议：
```

---

## Appendix D: Agent Orchestration Contract

所有创作 Skill 必须遵守。

### 不可违反项

- 不得单 Agent 完整生成章节。
- 不得跳过 Director。
- 不得跳过 Commercial Reviewer。
- 不得跳过 Continuity Auditor。
- 不得跳过 Anti-AI Voice Editor。
- 不得跳过 Obsidian Librarian 的记忆更新。
- 不得跳过 Agent Trace。

### 每章最低流程

```text
Director
-> Chapter Planner
-> Character Agent
-> Drafter
-> Commercial Reviewer
-> Continuity Auditor
-> Anti-AI Voice Editor
-> Polisher
-> Obsidian Librarian
-> Director Final Decision
```

### 记忆更新

每章后必须生成待确认更新：

- 人物变化。
- 关系变化。
- 伏笔新增。
- 伏笔回收。
- 时间线事件。
- 设定新增。
- 设定变更。
- 待用户确认问题。

未完成记忆更新，本章流程不得视为完成。

---

## Appendix E: Git And CI Rules

### Git

- 默认私有仓库。
- 功能分支开发。
- 禁止自动直推主干。
- 验收通过后中文 commit。
- 检测 `origin` 后 push。
- 没有 `origin` 就停止并提示配置。

### CI

GitHub Actions 必须检查：

- Python 单元测试。
- CLI smoke test。
- Markdown/YAML schema check。
- 样例 vault 初始化。
- dashboard 生成。
- package build。
- ruff lint。
- `vault/References` 不入库。
- publish-check smoke test。

---

## Appendix F: Acceptance Checklist

最终交付前必须全部满足。

### 工程

- [ ] `novelctl --help` 可运行。
- [ ] `python -m pytest` 通过。
- [ ] `ruff check .` 通过。
- [ ] `python -m build` 通过。
- [ ] GitHub Actions 配置完成。

### Vault

- [ ] `vault/` 可作为 Obsidian vault 打开。
- [ ] Dashboard 可读。
- [ ] 模板齐全。
- [ ] 男频/女频迷你样例存在。
- [ ] References 默认不入 Git。

### Agents And Skills

- [ ] 男频 Agent 完整。
- [ ] 女频 Agent 完整。
- [ ] 共享 Agent 完整。
- [ ] Skills 完整。
- [ ] Commands 降级入口存在。
- [ ] 每个创作 Skill 明确多 Agent 调用顺序。

### 创作规则

- [ ] 每章 2500 到 4000 有效字。
- [ ] 正文无完全空行。
- [ ] 英文比例不超过 1%。
- [ ] 单段不超过 180 有效字。
- [ ] 禁用句式可检查。
- [ ] 前三章禁止水文。
- [ ] 风险检查不通过时不允许 approved。

### 去 AI 味

- [ ] `/novel-deai` 存在。
- [ ] `novelctl deai` 可运行。
- [ ] 三稿并存。
- [ ] 不破坏商业节奏。
- [ ] 不新增重大剧情事实。

### 多 Agent

- [ ] 章节创作必须多 Agent。
- [ ] Agent Trace 生成。
- [ ] Director 裁决记录存在。
- [ ] 记忆更新待确认文件存在。

### GitHub

- [ ] 不直推主干。
- [ ] 阶段验收后提交。
- [ ] 中文 commit message。
- [ ] origin 存在时 push 当前分支。
- [ ] origin 不存在时停止并报告。

---

## References

- Claude Code Skills: https://code.claude.com/docs/en/skills
- Claude Code Commands: https://code.claude.com/docs/en/commands
- Claude Code Plugins Reference: https://code.claude.com/docs/en/plugins-reference
- Obsidian Core Plugins: https://obsidian.md/help/plugins
- Obsidian Bases: https://obsidian.md/help/bases
- Obsidian Properties: https://help.obsidian.md/properties
- Obsidian Graph View: https://help.obsidian.md/plugins/graph
- Obsidian Longform: https://community.obsidian.md/plugins/longform
- Obsidian Ima Vault: https://community.obsidian.md/plugins/ima
- 网络信息内容生态治理规定: https://www.gov.cn/zhengce/zhengceku/2020-11/25/content_5564110.htm
- 网络出版服务管理规定: https://www.nppa.gov.cn/xxgk/fdzdgknr/zcfg_210/bmgz_213/202112/t20211209_442163.html
- 网络暴力信息治理规定: https://www.cac.gov.cn/2024-06/14/c_1720043894161555.htm
