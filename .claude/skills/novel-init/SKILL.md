# /novel-init

## 用途

初始化新小说项目：创建 vault 目录结构、项目主文档、基础模板。

## 使用场景

- 开始一本新书的创作
- 使用方式：`/novel-init`

## 输入格式

用户需提供：
- 书名
- 题材
- 频道（male / female）
- 一句话核心创意

## 多 Agent 调用顺序

```
1. Program Operator → 执行 novelctl init-vault
2. Market Architect (male/female) → 生成市场定位报告
3. Worldbuilder (male/female) → 生成世界观设定
4. Character Architect (male/female) → 生成人物卡
5. Plot Architect (male/female) → 生成卷纲 + 前30章精纲
6. Obsidian Librarian → 整理索引和双链
7. Program Operator → 生成书籍圣经
```

## 输出文件

- `vault/01_Projects/<book>/` 项目主文档
- `vault/02_Characters/<book>/` 人物卡
- `vault/03_Worldbuilding/<book>/` 世界观设定
- `vault/04_Plot/<book>/` 大纲和精纲
- `vault/00_Dashboard/Dashboard.md` 更新后的仪表盘

## 自动检查

- 书籍圣经是否包含所有必要项（书名、简介、卖点、读者、主线、主角、配角、反派、世界观、规则、卷纲、前30章精纲、风险边界、禁写内容、商业节奏策略）
- 所有必需 Agent 是否被调用
- Agent Trace 是否生成

## 失败处理

- 任一 Agent 失败 → 报告 Director → 重新调度该步骤
- 自动重试最多 2 轮
- 2 轮后仍失败 → 停止并报告用户

## Agent Trace 要求

必须生成完整的项目初始化 Trace，包含所有 Agent 的输入输出摘要。
