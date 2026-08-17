# 第 063 晚：周验收：类型化工具调用协议状态机

## 具体目标

- 把 Ready、Awaiting、Closed 状态及合法事件建模为显式 ADT。
- 验证调用参数和结果类型，再执行状态迁移。
- 保留 append-only trace，并拒绝重复 result、未知 id 和关闭后调用。

## 前置编号

- 必须完成：057–062
- 闭卷入口问题：ADT 的穷尽分支与会话状态的合法转移怎样配合？

## 必读（20 分钟，已计入 60 分钟）

| 分钟 | 开放权威一手材料与版本 | 精确章节、页码或页内标题 | 阅读问题 |
|---:|---|---|---|
| 5–15 | [Model Context Protocol，Architecture](https://modelcontextprotocol.io/docs/learn/architecture) | “Core components”, “Protocol layer”, “Lifecycle” 页内标题 | 请求 id、能力协商和生命周期分别约束什么状态？ |
| 15–25 | [MCP specification 2025-06-18，Tools](https://modelcontextprotocol.io/specification/2025-06-18/server/tools) | “Listing tools”, “Calling tools”, “Tool result” 与 JSON Schema 定义 | 协议错误与工具执行错误为何需要不同表示？ |

只读指定边界；链接均为大学官方讲义、作者版本或正式论文页面。

## 导读

本周的 proof-as-program、索引类型和 session duality 汇合到一个小型工具协议。Python 版本在运行时检查；在真正的依赖/会话类型语言中，可把更多非法状态变成不可构造。

## 必做推导 / 证明

列出状态—事件转移矩阵；证明对所有可达状态，最多有一个 outstanding call。给出归纳基和每种事件的保持步骤。

必须保留判断形式和规则名；“凭直觉显然”不算完成。

## DeepSeek Harness / LLM 工程联系

这是直接的 Harness 工程预备：agent loop 产生调用，tool pipeline 返回结果，session log 记录 durable event。状态机让 replay 与在线执行遵守同一转移函数。

这是从形式概念到工程约束的映射；除明确指出外，不宣称 Harness 已静态证明这些性质。

## 严格 60 分钟

| 时间 | 工作 |
|---:|---|
| 0–5 | 回忆入口问题，写定义和反例 |
| 5–25 | 完成必读表并回答两个问题 |
| 25–38 | 手写推导或证明 |
| 38–55 | 运行 `practice.py`，再完成文件顶部的动手改造 |
| 55–60 | 按验收项自测并记录一个疑问 |

5 + 20 + 13 + 17 + 5 = 60 分钟。下面的延伸不得挤入本晚。

## 验收

- [ ] 正常 call/result/call/cancel/close 流程通过。
- [ ] 重复结果、错误 schema 和 Closed 后调用均失败。
- [ ] 动手改造：允许最多两个不同 id 的并发调用，并重写不变量。

## 可选延伸（不计时）

把 trace 序列化为 JSON 后重新 replay，确认最终状态一致。

