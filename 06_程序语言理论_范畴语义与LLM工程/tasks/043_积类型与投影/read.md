# 第 043 晚：积类型、pair 与投影

## 学习目标

- 为 pair、fst、snd 写语法/值/类型/归约规则。
- 推导积类型的 canonical form。
- 实现左到右 CBV pair 求值。

## 前置任务

- 第 038–042 晚的典范形式与类型安全。

## 必读材料（计入今晚 60 分钟）

| 分钟 | 材料 | 版本 | 精确范围 | 带着问题读 |
|---:|---|---|---|---|
| 19 | [Software Foundations — MoreStlc](https://softwarefoundations.cis.upenn.edu/plf-current/MoreStlc.html) | PLF current，页面快照 2026-01 | “Pairs” 从语法到 T_Pair/T_Fst/T_Snd 解释结束 | 哪些 value side condition 强制左到右？ |
| 7 | [PLFA — More](https://plfa.github.io/22.08/More/) | 22.08 | “Products” 的 syntax、reduction、typing rules | 积的 introduction 与两个 elimination 如何配对？ |

## 精读导引

把 pair 看作积的 introduction，fst/snd 看作两个 elimination。投影只有在被投影项化成 pair value 后才 β 化简；对非 pair 的投影应由类型检查提前排除。

## 必须完成的推导

1. 推导 `Γ⊢(t,u):A×B`。
2. 推导 `fst (v,w)→v` 并验证前后类型 A。
3. 陈述 canonical form：若 `v:A×B` 且 v 是值，则 `v=(v1,v2)`。

结论类型：【保守扩展】加入积类型后，新增 cases 仍可保持 progress/preservation。

## 与 DeepSeek Harness / LLM 工业应用的联系

直接联系：工具经常返回多个同时存在的结果字段；积类型保证每个分量都存在且可独立投影。它不同于“成功或失败”二选一，后者属于下一晚的和类型。

## 60 分钟安排

| 环节 | 分钟 |
|---|---:|
| 必读材料 | 26 |
| 规则与 canonical 推导 | 12 |
| 完成 pair 检查/求值 | 18 |
| 验收 | 4 |
| **合计** | **60** |

## 验收标准

- 写出 pair 与两个 projection 的 typing rule。
- fst 正例保持类型；非 pair 投影被拒绝。
- 单元素不可作 pair 的边界由 AST 类型体现。

## 可选延伸

- 实现 n 元 tuple，并比较嵌套二元积的结合同构。

