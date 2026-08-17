# 第 035 晚：不动点、发散与有界求值

## 学习目标

- 推导自应用 `Ω` 的一步自循环。
- 理解不动点组合子为何能表达递归。
- 实现区分 done 与 out-of-gas 的安全求值接口。

## 前置任务

- 第 032 晚“CBN 与求值策略对比”。
- 第 034 晚“Church 数与高阶编码”。

## 必读材料（计入今晚 60 分钟）

| 分钟 | 材料 | 版本 | 精确范围 | 带着问题读 |
|---:|---|---|---|---|
| 15 | [PLFA — Untyped](https://plfa.github.io/22.08/Untyped/) | 22.08 | “Naturals and fixpoint” 中 `μ f` 的具名定义及 `μ f → f (μ f)` 推导 | 递归名字怎样由自应用生成？ |
| 11 | [PLFA — Untyped](https://plfa.github.io/22.08/Untyped/) | 22.08 | “Evaluation”：Gas、Finished、eval，读到第一个 evaluator example 前 | 为什么 API 要把预算耗尽编码进结果？ |

## 精读导引

先手推 `Ω=(λx.xx)(λx.xx) → Ω`。再把 `μ f → f(μ f)` 看成展开方程，不要误认为所有 `f` 都会终止。宿主 Python 是 eager，直接 Y 会递归爆栈；实验用适配 eager 的 Z 组合子与显式 gas。按指定 PLFA evaluator 的约定，`gas zero` 不再调用一步函数，即使当前项碰巧已正规也返回 `out-of-gas`。

## 必须完成的推导

1. 写出 Ω 的完整一次 β 替换。
2. 推导 `μ f → f(μ f)`。
3. 证明有限 gas 返回 out-of-gas 不能逻辑推出“永不终止”。

结论类型：【可证明事实】Ω 发散可由自循环证明；【实验结果】任意特定 gas 耗尽只说明该预算内未完成。

## 与 DeepSeek Harness / LLM 工业应用的联系

这是直接工程联系：solver/agent 必须有步数、时间或 token 预算，并将预算耗尽作为一等结果；否则循环工具调用会挂死评测。结果状态不能伪装成语义失败。

## 60 分钟安排

| 环节 | 分钟 |
|---|---:|
| 必读材料 | 26 |
| Ω 与 μ 推导 | 12 |
| 完成有界实验 | 18 |
| 验收 | 4 |
| **合计** | **60** |

## 验收标准

- 能区分发散证明与 timeout 观测。
- Z 组合子算出小 factorial。
- Ω 在固定预算内返回明确 out-of-gas，且脚本不挂起。

## 可选延伸

- 为 evaluator 添加 cycle detection，比较它与 gas 的 soundness/completeness 边界。
