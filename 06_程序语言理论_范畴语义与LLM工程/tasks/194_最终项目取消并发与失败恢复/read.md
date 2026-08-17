# 第194晚：最终项目——取消、并发与失败恢复

## 目标与前置

- 目标：实现有界调度、exclusive barrier、模型序提交、abort drain 与 retry 分类。
- 前置：第187、189晚、Promise 状态概念。

## 计入 60 分钟的必读

| 分钟 | 材料 | 版本 | 精确范围 | 问题 |
|---:|---|---|---|---|
| 20 | [tool-calls.ts](https://github.com/deepseek-ai/deepseek-harness/blob/47f943859bef60e4160492346772ded9b24f765a/packages/core/agent-loop/src/tool-calls.ts#L104-L229) | Harness 47f943859bef60e4160492346772ded9b24f765a | path packages/core/agent-loop/src/tool-calls.ts；L104–229；symbols runGroup、commitReady、appendSkippedToolCall；checked_at 2026-08-15 | scheduler failure 与用户 abort 为何不同？ |

## 阅读导引

把 classify、dispatch、settle、commit 四阶段分开；只允许 dispatch overlap。记录 abort 后不再补充任务、等待 started、为 unstarted 造可回放结果。

## 核心推导

并发完成序不稳定，但 commit 按输入索引稳定。retry 只适用于明确 transient 且 effect 未提交的失败；未知副作用后盲重试可能重复操作。

## 工业联系与事实标签

- [THEOREM] 有限 started 集合且每个最终 settle 时，drain 终止。
- [EMPIRICAL] 固定源码区分 abort synthetic results 与 internal scheduler failure 不伪造结果。
- [INFERENCE] 工具需声明 idempotency key/side-effect phase 才能安全自动 retry。
- [OPEN] 分布式 exactly-once 一般不能由进程内 scheduler 单独保证。

## 严格 60 分钟

- 0–5：核对固定 SHA；5–25：必读；25–35：运行 `practice.ts` barrier/abort 预检；35–55：在真实 capstone spec 注入并行完成乱序、exclusive barrier、用户 abort 与 scheduler failure；55–60：保存提交顺序 trace 和 Vitest 输出。

## 验收

预检覆盖顺序、abort、exclusive、零任务；真实 checkout spec 证明模型序提交、barrier 不重叠、abort drain 与 internal failure 分类，并提交 SHA、diff、命令和 trace。

## 可选延伸

用 Promise mock 模拟不同完成序，不计时。
