# 第186晚：Harness Session 事件溯源与 Surface

## 目标与前置

- 目标：审计 append-only events、派生 surface、replacement 与历史重建。
- 前置：event sourcing、不可变日志、图投影。

## 计入 60 分钟的必读

| 分钟 | 材料 | 版本 | 精确范围 | 问题 |
|---:|---|---|---|---|
| 13 | [session/src/index.ts：append 提交](https://github.com/deepseek-ai/deepseek-harness/blob/47f943859bef60e4160492346772ded9b24f765a/packages/core/session/src/index.ts#L519-L620) | Harness 47f943859bef60e4160492346772ded9b24f765a | path packages/core/session/src/index.ts；定向读 L519–534、L535–620；symbols Session.events/seq/append；checked_at 2026-08-15 | `validateNext` 后，哪一行才把 candidate 提交为 durable fact？ |
| 5 | [surface.ts：replacement range](https://github.com/deepseek-ai/deepseek-harness/blob/47f943859bef60e4160492346772ded9b24f765a/packages/core/session/src/surface.ts#L230-L250) | 同一 commit | path packages/core/session/src/surface.ts；L230–250；symbol replacementRange；checked_at 2026-08-15 | replacement 为何留在原来的 surface 位置？ |
| 7 | [surface.ts：验证与折叠](https://github.com/deepseek-ai/deepseek-harness/blob/47f943859bef60e4160492346772ded9b24f765a/packages/core/session/src/surface.ts#L302-L374) | 同一 commit | path packages/core/session/src/surface.ts；L302–374；symbols planSurfaceEvent、applySurfaceEvent、foldSurface；checked_at 2026-08-15 | replacement 怎样 shadow 旧节点而不改写日志？ |

## 阅读导引

先追一个 user→assistant→tool call/result 序列，再追 replacement 事件。分别记录 event seq、sourceEventSeqs、surface nodes 与 derived messages。

## 核心推导

日志只追加，surface 是纯投影；replacement 通过引用/遮蔽改变可见历史，而不是删除旧事件。这样保留审计证据，同时允许压缩后的模型视图改变。

## 工业联系与事实标签

- [THEOREM] 若 reducer 确定，相同有序日志产生相同 surface。
- [EMPIRICAL] 固定源码把 session log 与 model-visible surface 分离；该提交的两个源码文件分别为 1098/435 行。
- [INFERENCE] 数据迁移必须版本化 event schema 与 projection，不能只存最终 messages。
- [OPEN] 长期日志的压缩、隐私删除与不可篡改审计之间存在政策冲突。

## 严格 60 分钟

- 0–5：画日志；5–30：两组局部行段精读；30–40：运行 `practice.ts` 回放预检；40–55：在固定 checkout 追踪一个 replacement fixture，记录 event seq、surface nodes 与 `foldSurface` 结果；55–60：保存追踪。

## 验收

`practice.ts` 的 append/replacement/未知引用/空日志断言通过；真实 checkout 追踪含固定 SHA 和 path:line，并能指出事实源与派生视图。

## 可选延伸

审计 invariant.ts 的请求重建，不计时。
