# References

参考库 — IMA 和网络公开资料导入区。

**此目录除本 README 外默认不提交 Git。**

把腾讯 ima、Obsidian Ima Vault、公开试读结构笔记或人工整理的参考 Markdown 放到本目录的子目录中，再运行导入命令。

## 推荐目录

```text
vault/References/
├── README.md
├── ima-inbox/          # 腾讯 ima / Ima Vault 导出的 Markdown
├── public-notes/       # 公开资料的高层结构笔记
├── manual-notes/       # 你自己整理的题材、节奏、平台口味笔记
└── _processed/         # 已导入、已归档的本地资料
```

这些子目录里的内容会被 `.gitignore` 保护，不应进入 Git。

## 使用规则

- 只允许学习结构模式（开局、冲突密度、钩子类型、情绪曲线、爽点分布、节奏）
- 禁止保存可复用原文
- 禁止将参考原文写入 Agent 提示词
- 禁止摘录长段正文

## IMA 导入步骤

1. 在腾讯 ima 或 Obsidian Ima Vault 中导出 Markdown。
2. 将导出的 `.md` 文件放入 `vault/References/ima-inbox/`。
3. 运行：

```powershell
novelctl import-ima --source vault/References
novelctl extract-patterns
novelctl index
novelctl publish-check
```

4. 检查 Git 状态：

```powershell
git status --short
```

除 `vault/References/README.md` 外，不应出现 `vault/References/` 下的参考原文文件。

## 允许导入的内容

- 章节结构摘要
- 开局模型
- 冲突密度观察
- 钩子类型
- 情绪曲线
- 爽点分布
- 章节功能
- 叙述节奏
- 平台口味高层分析

## 禁止导入或提交的内容

- 长段小说原文
- 可复用对白或段落
- 未授权的完整章节合集
- 作者隐私、账号信息、读者隐私
- 任何希望提交到 Git 的参考原文
