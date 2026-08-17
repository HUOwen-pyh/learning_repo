# 第192晚：最终项目——事件日志、回放与分叉

## 目标与前置

- 目标：实现带 seq/hash 的 append-only log、确定 projection 与安全 fork seed。
- 前置：第161、186晚、哈希链概念。

## 计入 60 分钟的必读

| 分钟 | 材料 | 版本 | 精确范围 | 问题 |
|---:|---|---|---|---|
| 8 | [surface.ts：来源与范围验证](https://github.com/deepseek-ai/deepseek-harness/blob/47f943859bef60e4160492346772ded9b24f765a/packages/core/session/src/surface.ts#L196-L250) | Harness 47f943859bef60e4160492346772ded9b24f765a | path packages/core/session/src/surface.ts；L196–250；symbols assertProvenance、replacementRange；checked_at 2026-08-15 | replacement 如何引用较早 durable event 并覆盖当前位置范围？ |
| 12 | [surface.ts：确定回放](https://github.com/deepseek-ai/deepseek-harness/blob/47f943859bef60e4160492346772ded9b24f765a/packages/core/session/src/surface.ts#L302-L374) | 同一 commit | path packages/core/session/src/surface.ts；L302–374；symbols planSurfaceEvent、applySurfaceEvent、foldSurface；checked_at 2026-08-15 | 同一有序日志为何得到同一 nodes/replacements？ |

## 阅读导引

跟踪 sourceEventSeqs 和 replacement；定义 hash 输入的 canonical encoding。课程用简化 rolling hash 教学，不当作密码学防篡改。

## 核心推导

每个事件携带 seq 与 prev hash，验证可定位第一处顺序/内容篡改。fork 复制选定 prefix 的值快照，子日志从新 identity 开始，避免两个 writer 共享可变数组。

## 工业联系与事实标签

- [THEOREM] 若 hash 无碰撞且覆盖 prev+payload，任一历史修改会使后续链验证失败；本练习弱 hash 不满足密码学前提。
- [EMPIRICAL] 固定 Harness session surface 使用事件引用构造派生视图。
- [INFERENCE] 审计系统需真实密码哈希、schema version、签名和持久 store。
- [OPEN] 合规删除与不可篡改日志需要专门治理方案。

## 严格 60 分钟

- 0–5：核对固定 SHA；5–25：必读；25–35：运行 `practice.ts` 哈希链预检；35–55：在真实 capstone package 挂载 Session，调用 append/events/surface/foldSurface 覆盖追加、replacement、回放与非法 replacement；55–60：保存 trace 和定向 Vitest 输出。

## 验收

预检覆盖 append、tamper、fork independence、空日志；真实 checkout spec 覆盖 Session append/replacement/replay 与非法引用，并提交 SHA、diff、命令、trace。不得以 mini log 代替真实集成。

## 可选延伸

换 Web Crypto SHA-256，不计时。
