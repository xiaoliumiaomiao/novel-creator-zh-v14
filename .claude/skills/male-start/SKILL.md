# /male-start

## 用途

启动男频小说创作流程：生成完整书籍圣经（立项到前30章精纲）。

## 使用场景

- 开始一本男频新书
- 使用方式：`/male-start`

## 输入格式

用户需提供：
- 书名
- 题材（玄幻/都市/脑洞/悬疑/历史/科幻/游戏/修仙）
- 一句话核心创意
- 可选：目标字数、每日更新量

## 多 Agent 调用顺序

```
1. male-director → 启动创作流程
2. male-market-architect → 市场定位报告
3. male-worldbuilder → 世界观设定
4. male-character-architect → 人物体系
5. male-plot-architect → 卷纲 + 前30章精纲
6. male-commercial-reviewer → 商业策略审查
7. male-continuity-auditor → 设定一致性审查
8. obsidian-librarian → 记忆索引
9. male-director → 汇总输出书籍圣经
```

## 输出文件

- `vault/01_Projects/<book>/` 项目主文档
- `vault/02_Characters/<book>/` 人物卡
- `vault/03_Worldbuilding/<book>/` 设定
- `vault/04_Plot/<book>/` 大纲精纲
- `vault/00_Dashboard/Agent_Traces/` 完整 Trace

## 自动检查

- 书籍圣经完整性：书名、简介、核心卖点、目标读者、平台口味、主线、主角、配角、反派、世界观、规则限制、分卷规划、前30章精纲、风险边界、禁写内容、商业节奏策略
- 爽点策略是否符合男频定位
- 前三章是否快速进入主冲突

## 失败处理

- 自动重试最多 2 轮
- 评分 < 85 自动返修
- 返修后仍不达标报告用户

## Agent Trace 要求

完整记录所有 Agent 的输入输出，包括 Director 的调度决策。
