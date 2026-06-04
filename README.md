# Novel Creator ZH V14.0

中文网文工业化创作工具集 — 供 Claude Code 在实际创作小说时调用多个专职 Agent 协作完成立项、设定、大纲、章节、正文、审稿、去 AI 味、修订、复盘和发布前检查。

## 创作定位

- 中文网文，番茄/七猫口味优先
- 男频/女频完全双套 Agent 体系
- 支持人主导模式和高自动批量模式
- 高自动批量模式每章后必须停下审阅

## 安装

```bash
# 克隆仓库（私有）
git clone <your-repo-url>
cd novel-creator-zh-v14.0

# 安装
pip install -e ".[dev]"
```

## 快速开始

```bash
# 初始化 Obsidian vault
novelctl init-vault

# 用 Obsidian 打开 vault/ 目录作为知识中枢
```

## IMA Skills 配置

项目已安装 `.claude/skills/ima-skill/`，用于连接 ima 知识库和笔记 OpenAPI。

使用前需要在本机配置凭证，凭证不要提交 Git：

```powershell
New-Item -ItemType Directory -Force "$env:USERPROFILE\.config\ima"
Set-Content "$env:USERPROFILE\.config\ima\client_id" "你的 Client ID"
Set-Content "$env:USERPROFILE\.config\ima\api_key" "你的 API Key"
```

也可以使用环境变量：`IMA_CLIENT_ID` / `IMA_API_KEY`，或兼容变量 `IMA_OPENAPI_CLIENTID` / `IMA_OPENAPI_APIKEY`。

凭证配置完成后，可通过 ima skill 搜索知识库、上传资料，再将导出的 Markdown 或结构笔记放入 `vault/References/ima-inbox/`，运行 `novelctl import-ima --source vault/References` 提炼结构模式。

## Obsidian 插件建议

### 核心插件（内置）
- Bases
- Properties view
- Graph view
- Canvas
- Backlinks
- Templates
- Word count

### 社区插件
- Longform：可选编排
- Ima Vault：腾讯 ima 导入
- Dataview：只读可选

## Claude Code 使用方式

本工具集通过 Claude Code 的 Agent/Skill/Command 体系运行：

- `.claude/agents/` — 专职 Agent 定义（男频/女频/共享）
- `.claude/skills/` — 创作工作流 Skill
- `.claude/commands/` — 降级入口

创作期必须使用多 Agent 编排，禁止单 Agent 包办整条创作链路。

## CLI 使用方式

```bash
novelctl --help                  # 查看所有命令

novelctl init-vault              # 初始化 vault
novelctl import-ima              # 导入参考库
novelctl index                   # 构建索引
novelctl extract-patterns        # 提炼写作模式
novelctl score-chapter <文件>     # 章节评分
novelctl deai <文件>             # 去 AI 味
novelctl lint                    # 硬规则检查
novelctl dashboard               # 生成仪表盘
novelctl publish-check           # 发布前总闸门
novelctl git-sync                # 安全 Git 同步
```

## GitHub 推送规则

- 默认私有仓库
- 功能分支开发，禁止直推主干
- 阶段验收通过后中文 commit
- 检测 origin 后 push；无 origin 时停止并提示配置

## 参考库版权与隐私边界

- `vault/References/` 默认不提交 Git
- 只允许学习结构模式（开局、冲突密度、钩子类型、情绪曲线、爽点分布、节奏）
- 禁止保存可复用原文，禁止将参考原文写入 Agent 提示词
