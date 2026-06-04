# /novel-deai

## 用途

对指定文件进行去 AI 味处理，输出三稿。

## 使用场景

- 单章去 AI 味
- 批量去 AI 味
- 全书去 AI 味
- 使用方式：`/novel-deai <file.md> --mode detail-light`

## 输入格式

- 文件路径（必选）
- 处理模式（--mode）：
  - `expression-only`：只改表达，不新增信息
  - `detail-light`：补动作、感官、心理毛刺、小反应
  - `dramatic-boost`：增强小冲突、小反应、段落钩子（标注新增处）

## 多 Agent 调用顺序

```
1. anti-ai-voice-editor → 执行去AI味处理
2. male/female-commercial-reviewer → 验证商业节奏未被破坏
3. Program Operator → 执行 novelctl deai
4. anti-ai-voice-editor → 输出三稿
```

## 输出文件

- 三稿：`<原文件名>.original.md` / `<原文件名>.natural.md` / `<原文件名>.web-serial.md`
- 去 AI 味评分（双评分：清单评分 + 读者视角评分）

## 自动检查

- 三稿是否完整
- 商业节奏是否保留
- 是否新增重大剧情事实（不应新增）
- dramatic-boost 模式是否标注新增处

## 失败处理

- 处理失败 → 保留原稿，报告错误
- 商业节奏被破坏 → 回退，降低处理强度

## Agent Trace 要求

记录处理模式、检测到的 AI 腔特征、评分变化。
