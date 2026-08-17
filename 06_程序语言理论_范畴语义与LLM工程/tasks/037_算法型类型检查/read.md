# 第 037 晚：从判断规则到算法型类型检查

## 学习目标

- 把 syntax-directed typing rules 翻译为递归算法。
- 为错误保留 AST 位置和期望/实际类型。
- 解释检查器何时 sound、何时 complete。

## 前置任务

- 第 036 晚“STLC 类型、上下文与判断规则”。

## 必读材料（计入今晚 60 分钟）

| 分钟 | 材料 | 版本 | 精确范围 | 带着问题读 |
|---:|---|---|---|---|
| 16 | [Software Foundations — Stlc](https://softwarefoundations.cis.upenn.edu/plf-current/Stlc.html) | PLF current，页面快照 2026-01 | “Typing” 全部规则与三个 typing examples | 哪些规则可由项的最外构造器唯一选择？ |
| 9 | [PLFA — Lambda](https://plfa.github.io/22.08/Lambda/) | 22.08 | “Typing” 中 lookup judgment 与 typing judgment 的规则声明 | 上下文查找失败应对应哪个无推导情形？ |

## 精读导引

对每个 AST 构造器写恰一个分支。带参数类型注解的 lambda 可直接综合箭头类型；`if` 要先检查 guard 为 Bool，再要求两分支相等。错误信息是算法产物，不属于数学判断本身。

## 必须完成的推导

1. 写出 `infer(Γ,x)`、`infer(Γ,λx:A.t)`、`infer(Γ,t u)` 伪代码。
2. 给 soundness 论证：算法返回 T 时可重建 `Γ⊢t:T`。
3. 给 completeness 论证思路：对 typing derivation 归纳，算法不会拒绝。

结论类型：【基础元定理】对本晚带注解 STLC，syntax-directed checker 对声明式规则 sound 且 complete。

## 与 DeepSeek Harness / LLM 工业应用的联系

直接联系：LLM 提议工具调用，检查器依据 schema/context 决定是否可执行。可解释错误应同时给期望类型、实际类型与位置，供重试或模型修复使用。

## 60 分钟安排

| 环节 | 分钟 |
|---|---:|
| 必读材料 | 25 |
| sound/complete 提纲 | 12 |
| 完成检查器 | 19 |
| 验收 | 4 |
| **合计** | **60** |

## 验收标准

- 每个构造器有明确输入/输出或错误。
- `if` 同时检查 guard 与分支一致性。
- 正例、guard 错误反例、同类型分支边界例通过。

## 可选延伸

- 把异常改为结构化 `TypeErrorInfo(path, expected, actual)`。

