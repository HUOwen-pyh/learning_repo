# 第180晚：Cordis 论文——动态组件演算

## 目标与前置

- 目标：理解 component、fiber、registry、target view、base calculus 与进行中转移。
- 前置：小步语义、状态机、并发交错。

## 计入 60 分钟的必读

| 分钟 | 材料 | 版本 | 精确范围 | 问题 |
|---:|---|---|---|---|
| 35 | [Cordis paper](https://github.com/cordiverse/paper/blob/948a07b369c62adb3b12e102458be5c18dfb69b9/paper.pdf) | 948a07b369c62adb3b12e102458be5c18dfb69b9 | path paper.pdf；§4.1–§4.3.4，Definitions 43–53 与规则表，PDF pp.28–38；checked_at 2026-08-15 | target view 变化怎样触发生命周期转移？ |

## 阅读导引

先抄写 component triple 和 fiber state，再读规则。每条规则记录：前置谓词、读取的 registry 字段、更新字段、产生的 effect。将 withdrawal、iteration、asynchrony、failure 分开。

## 核心推导

全局状态 γ 带 fiber registry。每一步只选择一个可用规则，形成交错语义；fiber 的 target view 由当前 providers 与 specification 决定。动态依赖变化不是任意回调，而是驱动 fiber 从 active 经过 withdraw/reapply 的规则。

## 工业联系与事实标签

- [THEOREM] 在小步关系中，一条执行轨迹是从初态出发的规则实例序列；其确定性需额外证明，不能由语法自动得到。
- [EMPIRICAL] §4 是抽象演算，不给现实调度开销。
- [INFERENCE] Agent 插件取消与热重载可用同一 fiber transition vocabulary 记录。
- [OPEN] 真实 JavaScript event loop 与抽象交错规则的对应需要实现层论证。

## 严格 60 分钟

- 0–5：画 registry；5–40：逐规则精读；40–54：运行小步机；54–58：故障注入；58–60：写一条规则判断。

## 验收

安装、等待、激活、撤销、失败边界断言；每次 step 只做一个转移。

## 可选延伸

手推两个 fiber 的全部交错，不计时。
