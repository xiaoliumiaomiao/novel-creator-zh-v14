# /novel-status

## 用途

查看小说项目整体状态。

## 使用场景

- 定期查看进度
- 使用方式：`/novel-status`

## 输入格式

- 项目名（可选，默认当前活跃项目）

## 多 Agent 调用顺序

```
1. Program Operator → 执行 novelctl dashboard
2. obsidian-librarian → 查询最新记忆状态
3. Program Operator → 展示仪表盘摘要
```

## 输出文件

- 更新后的 Markdown 仪表盘
- 更新后的 HTML 报表

## 自动检查

- 仪表盘是否包含所有必需项
- 数据是否最新

## 失败处理

- 仪表盘生成失败 → 报告错误日志

## Agent Trace 要求

记录状态查询时间。
