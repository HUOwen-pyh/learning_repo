# 第193晚：最终项目——工具与 LLM 流闭环

## 目标与前置

- 目标：把 mock LLM chunks 组装为消息，验证 tool call，经流水线执行并追加结果。
- 前置：第155、158、188、189晚。

## 计入 60 分钟的必读

| 分钟 | 材料 | 版本 | 精确范围 | 问题 |
|---:|---|---|---|---|
| 12 | [agent-loop/agent.ts](https://github.com/deepseek-ai/deepseek-harness/blob/47f943859bef60e4160492346772ded9b24f765a/packages/core/agent-loop/src/agent.ts#L313-L379) | Harness 47f943859bef60e4160492346772ded9b24f765a | path packages/core/agent-loop/src/agent.ts；L313–379；symbols step、BlockAssembler、assistant/message、executeToolCalls；checked_at 2026-08-15 | stream chunks 与完成消息为何分层记录？ |
| 8 | [tool-calls.ts](https://github.com/deepseek-ai/deepseek-harness/blob/47f943859bef60e4160492346772ded9b24f765a/packages/core/agent-loop/src/tool-calls.ts#L54-L102) | 同一 commit | path packages/core/agent-loop/src/tool-calls.ts；L54–102；symbols executeToolCalls、parseArguments；checked_at 2026-08-15 | invalid JSON 参数如何保留诊断？ |

## 阅读导引

画 request→chunks→assembler→assistant anchor→tool parse/validate/policy/body/result→next request。每层保留 correlation id。

## 核心推导

chunk 是传输增量，assistant message 是完成语义锚点；tool call 是结构块。只有完成锚点进入后续派生消息，原始 chunk 保留用于 UI/诊断。

## 工业联系与事实标签

- [THEOREM] 按 seq 排序且恰一次拼接可重建确定文本。
- [EMPIRICAL] 固定 agent.ts 对成功 finish 追加一个 assistant/message completion anchor。
- [INFERENCE] provider adapter 应负责 wire translation，core 只消费规范 chunk。
- [OPEN] 断流恢复的 exactly-once 需要 provider resume token 或去重协议。

## 严格 60 分钟

- 0–5：核对固定 SHA；5–25：必读；25–35：运行 `practice.ts` 预检；35–55：在真实 capstone package 注册 LlmAdapter test double 与真实 Tool，经 `ctx.llm`、AgentLoop、BlockAssembler、ToolRuntime 跑一轮；55–60：保存 session events 与 Vitest 输出。

## 验收

预检覆盖文本、工具、乱序、空流；真实 checkout 的定向 spec 证明 provider chunk→completion anchor→工具结果→下一轮，并提交 SHA、diff、命令与 session event trace。

## 可选延伸

加入 usage 与 max-token finish，不计时。
