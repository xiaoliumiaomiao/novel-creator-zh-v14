# /novel-audit

## 用途

对已完成或进行中的小说进行全面审计。

## 使用场景

- 定期质量审查
- 发布前最终审查
- 使用方式：`/novel-audit`

## 输入格式

- 指定项目名
- 审计范围（全部 / 最近 N 章 / 指定章节范围）

## 多 Agent 调用顺序

```
1. male/female-director → 启动审计流程
2. male/female-commercial-reviewer → 商业节奏审查
3. male/female-continuity-auditor → 连续性审查
4. anti-ai-voice-editor → 去AI味评估
5. corpus-analyst → 与参考库对标
6. Program Operator → 执行 novelctl publish-check
7. Director → 汇总审计报告
```

## 输出文件

- 审计报告（含各维度评分、问题清单、改进建议）
- 审计 Trace

## 自动检查

- `novelctl publish-check`
- 硬规则全量检查
- 风险全量审查
- 参考库泄漏检查

## 失败处理

- 发现风险 → 标记并降险
- 评分不达标 → 列出改进建议
- 参考库泄漏 → 立即清理

## Agent Trace 要求

完整审计 Trace。
