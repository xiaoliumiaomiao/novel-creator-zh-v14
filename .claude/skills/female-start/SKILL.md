# /female-start

## 用途

启动女频小说创作流程：生成完整书籍圣经（立项到前30章精纲）。

## 使用场景

- 开始一本女频新书
- 使用方式：`/female-start`

## 输入格式

用户需提供：
- 书名
- 题材（现言/古言/重生/甜宠/虐恋/年代/悬疑/幻想）
- 一句话核心创意
- 可选：目标字数、每日更新量

## 多 Agent 调用顺序

```
1. female-director → 启动创作流程
2. female-market-architect → 市场定位报告
3. female-worldbuilder → 世界观设定
4. female-character-architect → 人物体系
5. female-plot-architect → 卷纲 + 前30章精纲
6. female-commercial-reviewer → 商业策略审查
7. female-continuity-auditor → 设定一致性审查
8. obsidian-librarian → 记忆索引
9. female-director → 汇总输出书籍圣经
```

## 输出文件

- `vault/01_Projects/<book>/` 项目主文档
- `vault/02_Characters/<book>/` 人物卡（女主、男主、配角、反派）
- `vault/03_Worldbuilding/<book>/` 设定
- `vault/04_Plot/<book>/` 大纲精纲
- `vault/00_Dashboard/Agent_Traces/` 完整 Trace

## 自动检查

- 书籍圣经完整性
- 情感节奏是否符合女频定位
- 男主是否有足够苏感和身份张力
- 前三章是否快速建立情感期待

## 失败处理

- 自动重试最多 2 轮
- 评分 < 85 自动返修
- 返修后仍不达标报告用户

## Agent Trace 要求

完整记录所有 Agent 的输入输出，包括 Director 的调度决策。
