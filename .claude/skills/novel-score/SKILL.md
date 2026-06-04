# /novel-score

## 用途

对指定章节或全书进行多维度评分。

## 使用场景

- 检查单章质量
- 全书质量评估
- 使用方式：`/novel-score <chapter-file>`

## 输入格式

- 章节文件路径
- 可选项：评分维度过滤

## 多 Agent 调用顺序

```
1. Program Operator → 执行 novelctl score-chapter
2. male/female-commercial-reviewer → 追加商业评审意见
3. male/female-continuity-auditor → 追加连续性意见
4. Program Operator → 汇总评分
```

## 输出文件

- 评分报告（含各维度得分和改进建议）
- 更新后的仪表盘

## 自动检查

- 所有评分维度是否覆盖
- 评分是否 ≥ 85

## 失败处理

- 文件不存在 → 报告错误
- 评分 < 85 → 列出具体改进项

## Agent Trace 要求

记录评分过程和评审意见。
