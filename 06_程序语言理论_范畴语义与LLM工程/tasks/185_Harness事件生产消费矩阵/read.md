# 第185晚：Harness 事件生产—消费矩阵

## 目标与前置

- 目标：从具体 loop 源码建立 turn/step/request/stream/tool 事件的 producer、consumer、mode 与 durable 性矩阵。
- 前置：事件总线、ReAct、waterfall。

## 计入 60 分钟的必读

| 分钟 | 材料 | 版本 | 精确范围 | 问题 |
|---:|---|---|---|---|
| 10 | [event-producer-consumer.md](https://github.com/deepseek-ai/deepseek-harness/blob/47f943859bef60e4160492346772ded9b24f765a/docs/event-producer-consumer.md#L1-L71) | Harness 47f943859bef60e4160492346772ded9b24f765a | path docs/event-producer-consumer.md；L1–L71；表中 durable session、agent live、capability event 的 producer/consumer/mode；checked_at 2026-08-15 | 矩阵声称的 producer 能否在源码找到？ |
| 8 | [agent-loop/agent.ts：请求与流](https://github.com/deepseek-ai/deepseek-harness/blob/47f943859bef60e4160492346772ded9b24f765a/packages/core/agent-loop/src/agent.ts#L313-L379) | 同一 commit | path packages/core/agent-loop/src/agent.ts；L313–L379；symbols step、agent/request、assistant/chunk、assistant/message、executeToolCalls；checked_at 2026-08-15 | 哪些是持久事实，哪个是 waterfall？ |
| 7 | [agent-loop/agent.ts：轮次边界](https://github.com/deepseek-ai/deepseek-harness/blob/47f943859bef60e4160492346772ded9b24f765a/packages/core/agent-loop/src/agent.ts#L227-L311) | 同一 commit | path packages/core/agent-loop/src/agent.ts；定向只读 L227–275 与 L277–311；symbols turn、agent/turn-stopping、turn/start/end；checked_at 2026-08-15 | 为什么被拒绝的首步仍有 turn boundary？ |

## 阅读导引

只做调用点审计：每遇 append/emit/waterfall/dispatch 写一行矩阵，标 producer、payload、返回是否影响控制流、是否进入 session log。不要仅凭事件名猜语义。

## 核心推导

通知型事件不改变主流程；waterfall/bail 的返回值成为控制输入；durable session event 可重放而普通控制事件未必。一次调用链可同时产生两类事件，但职责不同。

## 工业联系与事实标签

- [THEOREM] 若消费者返回值被忽略，则它不能经该返回通道改变生产者状态（仍可能有外部副作用）。
- [EMPIRICAL] 固定 agent.ts 的 loop 从 session log 派生请求，并在插件 checkpoint 间推进。
- [INFERENCE] 生成 producer-consumer 矩阵可发现“事件已声明但无人生产/消费”的漂移。
- [OPEN] 第三方消费者的时延预算与隔离不由事件类型本身保证。

## 严格 60 分钟

- 0–5：建表头；5–30：读官方矩阵并核对两组调用点；30–40：运行 `practice.ts` 孤儿检查预检；40–55：在固定 checkout 用 `rg "append\(|waterfall\(|emit\(|serial\("` 核对至少 8 个矩阵行；55–60：保存带 path:line 的差异表。

## 验收

`practice.ts` 覆盖已连接/孤儿/空图；真实 checkout 差异表至少 8 个事件，每行含 producer、consumer、mode、durable、path:line；两份证据都通过才完成。

## 可选延伸

对照 docs/event-producer-consumer.md 固定提交，不计时。
