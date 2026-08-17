# 第 029 晚：无类型 lambda 的语法、值与正规形

## 学习目标

- 写出无类型 lambda 演算的三种项。
- 区分值、弱头正规形与 β 正规形。
- 判定开放项何时是 neutral term。

## 前置任务

- 第 022–028 晚的 AST、绑定与替换。

## 必读材料（计入今晚 60 分钟）

| 分钟 | 材料 | 版本 | 精确范围 | 带着问题读 |
|---:|---|---|---|---|
| 13 | [PLFA — Untyped](https://plfa.github.io/22.08/Untyped/) | 22.08 | 开头五条 variations；“Untyped is Uni-typed”；“Syntax” 至 “Terms and the scoping judgment” 结束 | untyped 为什么不等于不检查作用域？ |
| 12 | [PLFA — Untyped](https://plfa.github.io/22.08/Untyped/) | 22.08 | “Neutral and normal terms” 全节 | 为什么开放项 `x n` 可以正规却不是 lambda 值？ |

## 精读导引

把“值”视为求值策略的停机约定，把“正规形”视为没有任何允许的 redex。弱求值不进入 lambda，full normalisation 会进入；所以 `λx.((λy.y) x)` 可以是 CBV 值，却不是 β 正规形。

## 必须完成的推导

1. 给 `λx.((λy.y) x)` 分别标注 value、WHNF、normal。
2. 按互递归定义说明 neutral `n ::= x | n v` 与 normal `v ::= n | λx.v`。
3. 给出一个闭项 value 但非 β-normal 的例子。

结论类型：【定义边界】“已求值”必须相对于明确的归约策略解释。

## 与 DeepSeek Harness / LLM 工业应用的联系

这是基础层联系：Harness 的 solver 结束状态同样要区分“协议允许返回”“内部仍可化简”“预算耗尽”。lambda 的多个 normal 概念训练你在评测中声明停机判据。

## 60 分钟安排

| 环节 | 分钟 |
|---|---:|
| 必读材料 | 25 |
| 三类形态判定推导 | 12 |
| 完成 `practice.py` | 18 |
| 验收 | 5 |
| **合计** | **60** |

## 验收标准

- 能给出 value 与 β-normal 不等价的反例。
- 代码能在 lambda body 中发现 redex。
- 覆盖正规形正例、redex 反例、开放 neutral 边界例。

## 可选延伸

- 实现互递归 `is_neutral/is_normal`，对照当前直接扫描法。

