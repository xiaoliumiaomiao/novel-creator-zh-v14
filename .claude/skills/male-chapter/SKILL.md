# /male-chapter

## 用途

创作男频小说单章：从章纲到终稿，必须经过完整的多 Agent 链。

## 使用场景

- 人主导模式：用户提供详细章纲
- 高自动模式：用户只给一句目标
- 使用方式：`/male-chapter`

## 输入格式

- 人主导模式：提供精纲（场景、冲突、爽点、字数）
- 高自动模式：提供本章目标（一句话即可）

## 多 Agent 调用顺序

```
1. male-director → 读取上下文，拆解任务
2. male-chapter-planner → 生成/确认精纲
3. male-character-architect → 确认人物状态
4. male-drafter → 生成初稿
5. male-commercial-reviewer → 商业审稿
6. male-continuity-auditor → 连续性审查
7. anti-ai-voice-editor → 去AI味（三稿）
8. male-polisher → 精修终稿
9. obsidian-librarian → 更新记忆
10. male-director → 最终裁决，生成交付包
```

**严禁单 Agent 包办上述全部步骤。**

## 输出文件

- `vault/05_Chapters/<book>/第N章 标题.md` — 终稿（approved）
- 同目录下 `.original.md` / `.natural.md` / `.web-serial.md` 三稿
- 商业审稿报告
- 连续性审查报告
- 风险审查报告（如有触发）
- Agent Trace
- 待确认记忆更新

## 自动检查

- 硬规则（novelctl lint）
- 综合评分 ≥ 85
- 英文比例 ≤ 1%
- 有效字数 2500-4000
- 无禁用句式
- 无连续空行
- 段落 ≤ 180 字

## 失败处理

- 触犯硬规则 → 自动回修（最多 2 轮）
- 评分 < 85 → 返回 Drafter 修改（最多 2 轮）
- 2 轮后仍失败 → 停止并报告用户

## Agent Trace 要求

每章必须生成详细 Trace，包含每个 Agent 的输入摘要、输出摘要、采纳/拒绝记录、Director 裁决记录、退回与修复记录、待用户确认事项。
