# /novel-import-ima

## 用途

从 vault/References 导入 IMA Markdown 并生成结构卡。

## 使用场景

- 用户添加了新的参考材料到 References
- 使用方式：`/novel-import-ima`

## 输入格式

- 可选：指定源路径（默认 `vault/References`）

## 多 Agent 调用顺序

```
1. Program Operator → 执行 novelctl import-ima
2. corpus-analyst → 分析导入内容，生成结构卡
3. Program Operator → 执行 novelctl extract-patterns
4. obsidian-librarian → 更新索引
```

## 输出文件

- 结构卡（统计特征，不保存原文）
- 更新后的索引
- 导入报告

## 自动检查

- 参考库 Git 保护（不提交原文）
- 去重检查
- 结构卡只含统计数据

## 失败处理

- 文件无法读取 → 跳过并报告
- 去重冲突 → 保留最新版本

## Agent Trace 要求

记录导入文件数、结构卡生成数、跳过的文件。
