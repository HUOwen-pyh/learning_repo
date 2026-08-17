# 第188晚：Harness LLM 流与 Prompt 组装

## 目标与前置

- 目标：审计 prompt render，并真正走通 provider wire→`StreamChunk`→`BlockAssembler`→assistant message。
- 前置：流式块、模板解释器、缓存键。

## 计入 60 分钟的必读

| 分钟 | 材料 | 版本 | 精确范围 | 问题 |
|---:|---|---|---|---|
| 7 | [system-prompt render](https://github.com/deepseek-ai/deepseek-harness/blob/47f943859bef60e4160492346772ded9b24f765a/packages/core/system-prompt/src/index.ts#L188-L275) | Harness 47f943859bef60e4160492346772ded9b24f765a | path packages/core/system-prompt/src/index.ts；L188–L275；symbols renderPrompt、renderContextSections、interpolate；checked_at 2026-08-15 | 未知/未定义变量为何 fail loud？ |
| 4 | [LLM streaming：StreamChunk](https://github.com/deepseek-ai/deepseek-harness/blob/47f943859bef60e4160492346772ded9b24f765a/docs/subsystems/llm-streaming.md#L140-L166) | 同一 commit | path docs/subsystems/llm-streaming.md；L140–166；symbol StreamChunk；checked_at 2026-08-15 | index 如何关联交错 block？ |
| 4 | [LLM streaming：BlockAssembler](https://github.com/deepseek-ai/deepseek-harness/blob/47f943859bef60e4160492346772ded9b24f765a/docs/subsystems/llm-streaming.md#L243-L283) | 同一 commit | path docs/subsystems/llm-streaming.md；L243–283；symbol BlockAssembler；checked_at 2026-08-15 | assembler 对 malformed/开放 block 的边界是什么？ |
| 3 | [DeepSeek 映射与关闭 block](https://github.com/deepseek-ai/deepseek-harness/blob/47f943859bef60e4160492346772ded9b24f765a/packages/llm/llm-deepseek/src/translate.ts#L23-L70) | 同一 commit | path packages/llm/llm-deepseek/src/translate.ts；L23–70；symbols mapFinishReason、mapUsage、closeBlock；checked_at 2026-08-15 | wire finish/usage 怎样映射为中立类型？ |
| 7 | [DeepSeek translate](https://github.com/deepseek-ai/deepseek-harness/blob/47f943859bef60e4160492346772ded9b24f765a/packages/llm/llm-deepseek/src/translate.ts#L72-L170) | 同一 commit | path packages/llm/llm-deepseek/src/translate.ts；L72–170；symbols translate、open；checked_at 2026-08-15 | 为什么 usage/finish 延后到 `[DONE]`？ |

## 阅读导引

画两条会合的路径：prompt IR 经严格插值成 `system`；DeepSeek SSE 经 `translate` 成 provider-neutral chunks，再由 `BlockAssembler` 合成 blocks。记录 `block-start/delta/block-end/usage/finish` 的顺序不变量。

## 核心推导

prompt assembly 是有序 IR；render 是从 IR 到字符串的确定解释。严格单次插值避免未解析占位符和二次注入。任何较早 section 变化都会从该 token 位置破坏 KV 前缀复用。

## 工业联系与事实标签

- [THEOREM] 单次 prompt 替换避免二次注入；对索引完备且 start/delta/end 配对的 chunk 流，按 block index 折叠可确定性重建消息。
- [EMPIRICAL] 固定源码的 DeepSeek `translate` 把 provider wire 转成中立 chunk，并在 `[DONE]` 附近发出 usage/finish；AgentLoop 再交给 `BlockAssembler` 形成 completion anchor。
- [INFERENCE] prompt contribution 与 stream block 都应携带稳定 id/index，分别解释缓存失效与交错增量归属。
- [OPEN] provider tokenizer 的实际 cache hit、断流后的 exactly-once 恢复仍需遥测和 resume/dedup 协议。

## 严格 60 分钟

- 0–5：画双路径；5–30：按表定向精读；30–42：运行 `practice.ts` 的 wire/chunk/assembler 预检；42–55：在固定 checkout 找到 `translate` 和 `BlockAssembler` 对应 spec，运行一个含 text+tool-call+usage+finish 的定向测试；55–60：保存 chunk trace。

## 验收

`practice.ts` 断言 provider wire 翻译、交错 block 组装、usage-before-finish 和 prompt 严格插值；真实 checkout 定向 spec 通过并保存 chunk trace；只做 prompt 练习不算完成。

## 可选延伸

审计 LLM adapter 的 stream translate，不计时。
