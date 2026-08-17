# 第 041 晚：Preservation 保持性

## 学习目标

- 陈述 subject reduction/preservation。
- 按 reduction derivation 归纳分析 context 与 β cases。
- 逐步检查求值轨迹的类型不变量。

## 前置任务

- 第 039 晚“Progress 进展性”。
- 第 040 晚“弱化、重命名与替换引理”。

## 必读材料（计入今晚 60 分钟）

| 分钟 | 材料 | 版本 | 精确范围 | 带着问题读 |
|---:|---|---|---|---|
| 18 | [PLFA — Properties](https://plfa.github.io/22.08/Properties/) | 22.08 | “Preservation” theorem 与 proof，重点 application congruence 和 `β-ƛ` cases | β case 在哪一行调用 substitution？ |
| 8 | [Software Foundations — Types](https://softwarefoundations.cis.upenn.edu/plf-current/Types.html) | PLF current，页面快照 2026-01 | “Preservation” 小节的 theorem statement、proof idea 与 counterexample discussion | preservation 是否声称项的文本不变？ |

## 精读导引

定理说“类型不变”，不说值、大小或运行成本不变。ξ cases 对子归约使用归纳假设并重建外层 typing；β case 反演 T_App/T_Abs 后正好得到替换引理的两个 premise。

## 必须完成的推导

1. 写出 `Γ⊢t:T ∧ t→t′ ⇒ Γ⊢t′:T`。
2. 完成 β case 的 typing derivation 拼接图。
3. 给出一个 reduce 后 AST 大小改变但类型保持的例子。

结论类型：【类型安全核心定理】一步归约保持类型；由归纳可推广到多步轨迹。

## 与 DeepSeek Harness / LLM 工业应用的联系

直接联系：经过每次内部重写/调度后，工具轨迹仍应满足同一协议类型。持续检查可定位首个破坏不变量的 transformation，而不是等最终执行报错。

## 60 分钟安排

| 环节 | 分钟 |
|---|---:|
| 必读材料 | 26 |
| β 与 ξ proof cases | 13 |
| 完成轨迹检查器 | 17 |
| 验收 | 4 |
| **合计** | **60** |

## 验收标准

- 明确 theorem 是一步关系，能说明多步推广。
- 每个实际 step 前后 infer 类型相等。
- 多步正例、ill-typed 反例、值的零步边界通过。

## 可选延伸

- 保存每步所用规则，按规则分别统计 preservation 覆盖率。

