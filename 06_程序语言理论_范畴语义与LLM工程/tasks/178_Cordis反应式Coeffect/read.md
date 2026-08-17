# 第178晚：Cordis 论文——反应式 Coeffect

## 目标与前置

- 目标：理解 coeffect context、specification、notification、isolation 与 interception。
- 前置：依赖集合、有限映射、等价关系。

## 计入 60 分钟的必读

| 分钟 | 材料 | 版本 | 精确范围 | 问题 |
|---:|---|---|---|---|
| 32 | [Cordis paper](https://github.com/cordiverse/paper/blob/948a07b369c62adb3b12e102458be5c18dfb69b9/paper.pdf) | 948a07b369c62adb3b12e102458be5c18dfb69b9 | path paper.pdf；§3.2.1–§3.2.3，Definitions 22–31，PDF pp.17–22；checked_at 2026-08-15 | coeffect specification 如何决定“谁应被通知”？ |

## 阅读导引

为 key、value family、state、specification 与 operation 写类型。按 set 前后状态比较 declared keys；再分别画 isolation 改写可见空间、interception 改写访问操作。

## 核心推导

coeffect specification d 声明组件观察哪些上下文坐标。上下文从 σ 变为 σ' 时，仅当 d 上的观察发生相关变化才重算组件。reactive 不是轮询，而是 change→match spec→notify 的运行时协议。

## 工业联系与事实标签

- [THEOREM] 若 d 为空，则任意两个状态在 d 上的投影相同，因此无依赖变化通知需求。
- [EMPIRICAL] §3.2 给的是机制形式化，不提供生产吞吐测量。
- [INFERENCE] Harness 的 inject 可视为服务键上的 coeffect specification。
- [OPEN] 高频依赖抖动下的去抖、批处理和公平性不由抽象 specification 唯一决定。

## 严格 60 分钟

- 0–5：写依赖表；5–37：逐段精读；37–53：实现通知器；53–58：加入 isolate；58–60：总结 effect/coeffect 方向。

## 验收

相关键、无关键、空 specification 断言；能区分 isolation 与 interception。

## 可选延伸

用代理对象实现读取拦截，不计时。
