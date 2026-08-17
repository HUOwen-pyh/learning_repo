# 第189晚：Harness 工具流水线与安全策略

## 目标与前置

- 目标：审计 registry、executionMode、pre/execute/post/finalize/result 以及并行组的模型序提交。
- 前置：工具契约、策略 guard、并发池、AbortSignal。

## 计入 60 分钟的必读

| 分钟 | 材料 | 版本 | 精确范围 | 问题 |
|---:|---|---|---|---|
| 6 | [ToolRuntime 注册与 guard](https://github.com/deepseek-ai/deepseek-harness/blob/47f943859bef60e4160492346772ded9b24f765a/packages/core/tools/src/index.ts#L966-L1049) | Harness 47f943859bef60e4160492346772ded9b24f765a | path packages/core/tools/src/index.ts；L966–L1049；symbols register、restrict、guard；checked_at 2026-08-15 | 哪些注册是 effect-scoped？ |
| 11 | [ToolRuntime 执行阶段](https://github.com/deepseek-ai/deepseek-harness/blob/47f943859bef60e4160492346772ded9b24f765a/packages/core/tools/src/index.ts#L1372-L1556) | 同一 commit | path packages/core/tools/src/index.ts；定向读 L1372–1425、L1475–1556；symbols prepareExecution、dispatchScheduledExecution、finalizeScheduledExecution、finishScheduledExecution；checked_at 2026-08-15 | pre/guard/body/post/finalize/result 如何分层？ |
| 8 | [tool-calls 调度与有序提交](https://github.com/deepseek-ai/deepseek-harness/blob/47f943859bef60e4160492346772ded9b24f765a/packages/core/agent-loop/src/tool-calls.ts#L54-L150) | 同一 commit | path packages/core/agent-loop/src/tool-calls.ts；L54–L102 与 L104–L150；symbols executeToolCalls、parseArguments、runGroup.commitReady；checked_at 2026-08-15 | 并行执行为何仍按模型顺序提交？ |

## 阅读导引

先追一条成功调用，再追 guard deny、invalid args、body throw、abort-before-dispatch。分开 dispatch overlap 与 policy/result/context ordering；定位 synthetic result 的回放目的。

## 核心推导

pipeline 各层职责不同：参数验证证明形状，guard 决定权限，body 产生 canonical value，finalizer 渲染持久 content，result event 通知观察者。并行只重叠 body，提交序保持模型顺序以稳定会话。

## 工业联系与事实标签

- [THEOREM] 若并行结果按输入索引排序后提交，则提交序与完成时间无关。
- [EMPIRICAL] 固定 tool-calls.ts 将 exclusive call 作为 barrier，并对 skipped call 追加 ABORTED_BEFORE_DISPATCH 结果。
- [INFERENCE] permission/sandbox 插件应位于 pre-execute/guard，而非散落工具 body。
- [OPEN] 多资源调用的跨 sibling 安全分类在该 README 所述模型中仍有限制。

## 严格 60 分钟

- 0–5：画 pipeline；5–30：三个局部行段审计；30–40：运行 `practice.ts` 有序提交预检；40–55：在固定 checkout 运行 guard/abort/parallel 相关定向 spec，保存一条 deny 和一条 parallel trace；55–60：写层次故障表。

## 验收

`practice.ts` 的成功/deny/body 失败/空组/abort 断言通过；真实 checkout 定向 spec 通过，deny/parallel trace 能回标上表三个 path/symbol/range。

## 可选延伸

精读 tools tests 中 scheduler/guard 案例，不计时。
