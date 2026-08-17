# 第196晚：最终答辩与综合验收

## 目标与前置

- 目标：用一条端到端 trace 证明项目具备可逆组合、可回放会话、受控工具、取消和可测性质。
- 前置：完成第190–195晚。

## 计入 60 分钟的必读

| 分钟 | 材料 | 版本 | 精确范围 | 问题 |
|---:|---|---|---|---|
| 10 | [Agent loop 定向复习](https://github.com/deepseek-ai/deepseek-harness/blob/47f943859bef60e4160492346772ded9b24f765a/packages/core/agent-loop/src/agent.ts#L313-L379) | Harness 47f943859bef60e4160492346772ded9b24f765a | path packages/core/agent-loop/src/agent.ts；L313–379；symbols BlockAssembler、assistant/message、executeToolCalls；复用第193晚批注；checked_at 2026-08-15 | 最终证据如何连接 chunk、anchor 与 tool？ |
| 10 | [Tool scheduler 定向复习](https://github.com/deepseek-ai/deepseek-harness/blob/47f943859bef60e4160492346772ded9b24f765a/packages/core/agent-loop/src/tool-calls.ts#L104-L229) | 同一 commit | path packages/core/agent-loop/src/tool-calls.ts；只复核 L104–150、L201–229；symbols runGroup、commitReady、abort；checked_at 2026-08-15 | 最终 trace 如何证明工具结果顺序和取消语义？ |

## 阅读导引

做差距表：官方机制、你的对应、你的省略、风险。答辩只陈述被断言覆盖的性质；未做网络、OS sandbox、真实 provider、耐久数据库测试必须明确说未验证。

## 核心推导

综合验收是性质交集：Replay ∧ Rollback ∧ Policy ∧ Ordering ∧ Cancellation ∧ NoLeak。任一项失败即不通过；最终输出不是“代码能跑”，而是一组可复核证据。

## 工业联系与事实标签

- [THEOREM] 合取验收中任一必要性质为 false，则整体为 false。
- [EMPIRICAL] 本地 `practice.ts` 是 deterministic mock；毕业证据覆盖固定 SHA checkout 的 Cordis/Vitest 集成，但仍未覆盖真实 provider、网络、OS sandbox 或耐久数据库。
- [INFERENCE] 从这里进入工业前沿，应补 property-based tests、fault injection、sandbox、observability 和真实 benchmark。
- [OPEN] 自演化组件的形式验证、权限升级防护与线上治理仍是研究/工程前沿。

## 严格 60 分钟

- 0–5：核对固定 SHA；5–25：按表复核既有批注；25–45：在真实 Harness/npm workspace 运行 capstone 全部定向测试与一条端到端 trace；45–52：破坏一个 gate 确认失败；52–57：运行 `practice.ts` 证据非空预检；57–60：保存 SHA、diff、命令、输出并作三分钟答辩。

## 验收

毕业必须提交真实固定 SHA checkout 中可解析的 npm workspace package、Cordis 插件图、端到端 session/tool trace、全套定向测试输出和逐任务评测报告；六性质逐项有非空证据，任一 gate 失败则整体失败。`practice.ts` 只作预检，不能代替真实集成。

## 可选延伸

加入 property-based testing、fault injection 与真实 provider sandbox；不计时。
