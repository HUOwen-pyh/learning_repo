# 第 044 晚：和类型、注入与 case 分支

## 学习目标

- 实现 `inl/inr` 与 exhaustive case。
- 解释注入为何需要“另一侧类型”注解。
- 推导 case 两分支必须同结果类型。

## 前置任务

- 第 043 晚“积类型、pair 与投影”。

## 必读材料（计入今晚 60 分钟）

| 分钟 | 材料 | 版本 | 精确范围 | 带着问题读 |
|---:|---|---|---|---|
| 20 | [Software Foundations — MoreStlc](https://softwarefoundations.cis.upenn.edu/plf-current/MoreStlc.html) | PLF current，页面快照 2026-01 | “Sums” 从动机至 typing rules；继续读类型注解/uniqueness 解释段落 | `inl true` 的右侧类型为何无法从项本身推出？ |
| 6 | [PLFA — More](https://plfa.github.io/22.08/More/) | 22.08 | “Sums” 中 injection、case、reduction rules | case 的两个 binder 各是什么类型？ |

## 精读导引

积表示“同时有”，和表示“二者择一并带 tag”。case 是唯一安全消去方式：先看 tag，再只在对应分支绑定 payload。静态上两个分支必须汇合到同一结果类型。

## 必须完成的推导

1. 推导 `inl true : Bool+Bool`。
2. 推导 `case (inl true) of inl x⇒x | inr y⇒false → true`。
3. 说明遗漏 tag 或分支结果类型不同会破坏什么。

结论类型：【类型安全构造】显式 tag + exhaustive case 排除“把错误分支 payload 当成功值”。

## 与 DeepSeek Harness / LLM 工业应用的联系

直接联系：`Result<Success, Error>`、工具返回与解析失败都应建模为带 tag 的和，而非可空/混合字典。这样 evaluator 必须显式处理成功和失败路径。

## 60 分钟安排

| 环节 | 分钟 |
|---|---:|
| 必读材料 | 26 |
| case typing/β 推导 | 12 |
| 完成 sum 实验 | 18 |
| 验收 | 4 |
| **合计** | **60** |

## 验收标准

- 注入项携带另一侧类型。
- case 两分支结果类型相同。
- inl 正例、分支错型反例、inr 边界通过。

## 可选延伸

- 用 `A+Unit` 构造 Option，并实现 map。

