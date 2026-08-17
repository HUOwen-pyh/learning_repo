# 第 033 晚：Church 布尔与控制编码

## 学习目标

- 仅用函数编码 true、false 和 if。
- 通过 β 推导验证分支选择。
- 区分编码的行为契约与宿主语言的真假值。

## 前置任务

- 第 030 晚“β 归约与多步关系”。

## 必读材料（计入今晚 60 分钟）

| 分钟 | 材料 | 版本 | 精确范围 | 带着问题读 |
|---:|---|---|---|---|
| 11 | [PLFA — Untyped](https://plfa.github.io/22.08/Untyped/) | 22.08 | 章首至 “Syntax” 开头：重点读“only variables, abstraction, application; other constructs encoded” | “编码”与新增原语有何不同？ |
| 13 | [Stanford Encyclopedia of Philosophy — The Lambda Calculus](https://plato.stanford.edu/entries/lambda-calculus/) | 2023 substantive revision | §2.2 “Combinators” 表中 `T`/`F` 两行；§9.1.1 “Terms as logical constants” 从条件编码读至 `PAB` 的 true/false 两条归约结束 | 一个布尔值怎样以“选择器”的可观察行为定义？ |

## 精读导引

定义 `TRUE=λt.λf.t`、`FALSE=λt.λf.f`、`IF=λb.λt.λf.b t f`。逐个 β 化简；不要把名字 `TRUE` 当证明，真正契约是传入两个分支后返回哪一个。

## 必须完成的推导

1. `IF TRUE M N →* M`。
2. `IF FALSE M N →* N`。
3. 推出 `NOT=λb.b FALSE TRUE`，并验证两个输入。

结论类型：【表示】Church 布尔由消去行为刻画；其数据与控制流合一。

## 与 DeepSeek Harness / LLM 工业应用的联系

这是基础层联系：结构化选择器的语义由“给定候选后选谁”定义，而非字段名字。对 LLM 输出，Harness 也应通过行为/验证器判定契约，不能只相信模型生成的标签。

## 60 分钟安排

| 环节 | 分钟 |
|---|---:|
| 必读材料 | 24 |
| 三个 β 推导 | 13 |
| 完成惰性分支代码 | 18 |
| 验收 | 5 |
| **合计** | **60** |

## 验收标准

- 不使用宿主 `if` 定义 Church true/false 的选择行为。
- 未选分支 thunk 不被执行。
- true 正例、非法编码反例、false 边界例通过。

## 可选延伸

- 推导 AND、OR，并记录各需要多少次函数应用。
