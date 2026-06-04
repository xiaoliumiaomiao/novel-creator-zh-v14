# Agent Orchestration Contract (编排合同)

> 本文件为中文网文工业化创作工具集的强制性编排合同。
> 所有创作 Skill 和 Agent 必须遵守。违反合同的操作将被 `orchestration.py` 拒绝。

## 1. 不可违反项

- **不得单 Agent 完整生成章节。** 任何单个 Agent 不得执行从章纲到终稿的全部步骤。
- **不得跳过 Director。** 每次创作任务必须有 Director 参与调度。
- **不得跳过 Commercial Reviewer。** 每章初稿必须经过商业审稿。
- **不得跳过 Continuity Auditor。** 每章初稿必须经过连续性审查。
- **不得跳过 Anti-AI Voice Editor。** 每章必须经过去 AI 味处理。
- **不得跳过 Obsidian Librarian。** 每章完成后必须更新项目记忆。
- **不得跳过 Agent Trace。** 每章必须生成完整的 Agent 调用记录。

## 2. 每章最低流程

```
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

以上 10 个节点中，Director 出现两次（调度 + 最终裁决），其余 8 个专职 Agent 各出现一次。

## 3. 裁决优先级

```
商业节奏 > 法律/政治风险 > 设定一致性 > 人物动机 > 去AI味 > 文风精修
```

当 Agent 之间产生冲突时，Director 必须按此优先级裁决。

## 4. 记忆更新要求

每章完成后 Obsidian Librarian 必须生成待确认更新：

- 人物变化（新增能力、状态变化、性格发展）
- 关系变化（人物之间的关系更新）
- 伏笔新增（本章新埋的伏笔）
- 伏笔回收（本章回收的伏笔）
- 时间线事件（本章发生的时间节点）
- 设定新增（本章新增的世界设定）
- 设定变更（本章修改的世界设定）
- 待用户确认问题

未完成记忆更新，本章流程不得视为完成。

## 5. Agent Trace 要求

每章必须生成详细 Agent Trace，保存至：
`vault/00_Dashboard/Agent_Traces/<project>-ch<NNN>-trace.md`

每份 Trace 必须包含：
- 调用时间
- 项目名
- 章节号
- 调用 Agent 列表
- 每个 Agent 的输入摘要
- 每个 Agent 的输出摘要
- 采纳建议
- 拒绝建议及原因
- Director 裁决记录
- 退回与修复记录
- 待用户确认事项

## 6. 质量门槛

- 章节综合评分 ≥ 85 分
- 硬规则检查全部通过
- 风险审查通过
- 自动返修上限 2 轮
- 超过 2 轮仍不通过，停止并报告用户

## 7. 合同验证

`orchestration.py` 提供 `validate_orchestration_contract()` 函数，
在每次创作流程开始和结束时验证合同遵守情况。

违反合同项将导致：
1. 警告并记录
2. 阻止章节进入 `approved` 状态
3. 在 Agent Trace 中标记违规
