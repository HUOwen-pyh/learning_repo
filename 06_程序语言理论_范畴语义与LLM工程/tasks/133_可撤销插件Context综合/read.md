# 第 133 晚：可撤销插件 Context 综合

## 学习目标

- 把 service dependency、响应式激活和 disposer journal 合成一个小运行时。
- 用不变量定义“卸载干净”，而不是只看主返回值。

## 前置知识与关联任务

综合 127–132；回顾 089 的 event sourcing 与 074 的状态迁移检查。

## 必读材料（计入今晚 60 分钟）

| 分钟 | 材料 | 版本 | 精确范围 | 带着什么问题读 |
|---:|---|---|---|---|
| 10 | [Cordis Primer](https://github.com/deepseek-ai/deepseek-harness/blob/47f943859bef60e4160492346772ded9b24f765a/docs/cordis-primer.md) | `47f943…` | 全文 35 行，重点 Five Ideas 与 Practical Rules | 五个概念怎样组成一个生命周期闭环？ |
| 10 | [Cordis tutorial: lifecycle](https://github.com/deepseek-ai/deepseek-harness/blob/47f943859bef60e4160492346772ded9b24f765a/docs/cordis-tutorial/02-lifecycle-and-effects.md) | `47f943…` | 从 “Effects” 到章节验收输出 | 实例如何观察注册被自动撤销？ |

## 精读导引

这次把空间和时间两维合起来：Context 持有服务；插件声明依赖；满足后执行 apply；apply 的每次注册都返回 disposer；依赖消失或插件卸载时按逆序清理。验收快照至少包含 services、listeners、tools 和 active fibers。

## 必须完成的推导或证明

写三个状态不变量：active→requirements satisfied；registration owner active；unloaded owner has zero registrations。为每个不变量构造最小破坏例。

## 代码实战

完成 MiniContext：状态快照同时覆盖 `services/listeners/tools/active_fibers`；挂载 provider/consumer 后按依赖卸载。另让一个插件依次注册 listener、tool 后在 `apply` 中抛错，断言 journal 逆序回滚且四类状态与失败前完全相同。

## 与 DeepSeek Harness / LLM 工业应用的联系

这是进入真实 Cordis/Harness 前的核心微型模型。真实源码更复杂，但阅读时仍用同一组不变量追踪 service、effect 和 fiber。

## 60 分钟安排

- 0–5：闭卷列三条不变量。
- 5–25：精读 primer/tutorial。
- 25–48：运行并故障注入 MiniContext。
- 48–55：写最小破坏例。
- 55–60：阶段验收。

## 验收标准

- provider 删除与恢复流程正确。
- 全局 dispose 后四类可观察状态为空。
- `apply` 中途异常按注册逆序回滚，失败插件无任何残留。
- 能把每个断言映射到一条文字不变量。

## 可选延伸

阅读固定 `vendor/cordis/src/context.ts`；不计入今晚。
