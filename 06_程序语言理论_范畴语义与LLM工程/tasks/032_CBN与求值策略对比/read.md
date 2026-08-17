# 第 032 晚：CBN、CBV 与求值策略对比

## 学习目标

- 比较 call-by-name 与 call-by-value 的 β 前提。
- 找到两种策略终止行为不同的项。
- 用 step budget 做可重复的策略实验。

## 前置任务

- 第 031 晚“求值上下文与 CBV”。

## 必读材料（计入今晚 60 分钟）

| 分钟 | 材料 | 版本 | 精确范围 | 带着问题读 |
|---:|---|---|---|---|
| 14 | [PLFA — Untyped](https://plfa.github.io/22.08/Untyped/) | 22.08 | 章首关于 CBN/full normalisation 的五条对比；“Reduction step” 前导四点 | CBN 的 β 为何不要求实参 normal/value？ |
| 10 | [PLFA — Untyped](https://plfa.github.io/22.08/Untyped/) | 22.08 | “Evaluation” 从 Gas 到 `Finished` 的 `done/out-of-gas` 定义 | out-of-gas 能否推出永不终止？ |

## 精读导引

构造 `K I Ω`，其中 `K=λx.λy.x`、`Ω=(λx.xx)(λx.xx)`。CBN 不碰未用实参，CBV 必须先求 Ω。实验结果应表述为“CBV 在 N 步内未结束”，不是凭有限观测证明发散。

## 必须完成的推导

1. 手推 CBN 的 `K I Ω →* I`。
2. 展示 `Ω → Ω` 的一步自循环。
3. 写出 CBV 与 CBN 的 evaluation-context 文法差异。

结论类型：【定理/实验边界】标准 CBN 若有 β 正规形可找到它；有限 gas 耗尽本身只是实验结果，不是发散证明。

## 与 DeepSeek Harness / LLM 工业应用的联系

直接联系是惰性工具参数与预算：某参数若最终未被使用，提前执行可能浪费费用或触发副作用。Harness 中是否惰性必须由协议显式规定，不能从本例直接推广为“一律 CBN 更好”。

## 60 分钟安排

| 环节 | 分钟 |
|---|---:|
| 必读材料 | 24 |
| `K I Ω` 双策略推导 | 13 |
| 完成策略实验 | 18 |
| 验收 | 5 |
| **合计** | **60** |

## 验收标准

- 能解释两个策略的 β 前提差异。
- 同一项在 CBN 预算内结束、CBV 用尽预算。
- 正常项、发散候选反例、gas=0 边界均有断言。

## 可选延伸

- 加入 call-by-need memoization 并计数重复求值次数。

