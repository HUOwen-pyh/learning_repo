# 第 080 晚：PCF 类型的指称：值域与函数域

## 具体目标

- 把有限 Bool/Nat 域和箭头域表示为集合。
- 枚举有限函数空间并检查输入/输出成员关系。
- 区分数学函数域与宿主语言实现函数。

## 前置编号

- 必须完成：076、078
- 入口问题：为何函数类型不能仅解释为 Python 中任意 callable 的集合？

## 必读表（20 分钟，计入总时长）

| 分钟 | 开放权威一手材料与版本 | 精确章节、页码或锚点 | 阅读问题 |
|---:|---|---|---|
| 5–15 | [Andrew M. Pitts, Denotational Semantics（Cambridge 官方讲义）](https://www.cl.cam.ac.uk/teaching/1112/DenotSem/dens-notes-bw.pdf) | §5.6 pp.64–68 与 §6.1 “Denotations of types” pp.69–70 | 自然数域中的 bottom 表示什么观察？ |
| 15–25 | [PLFA，Denotational](https://plfa.inf.ed.ac.uk/Denotational/) | `Denotational` 章中 domains、values 与 function semantics 的定义 | 函数类型解释为什么还要满足连续性，而不只是总映射？ |

Pitts PDF 固定为 Cambridge 2011–12 课程讲义发布版；网页采用当前公开章版。页码按正文印刷页，只读规定范围。

## 导读

类型的指称为每个类型选择一个语义域。函数类型在域理论中是连续函数域；脚本用有限总函数作为可穷举近似，并明确这是简化模型。

## 必做推导或证明

对有限 `Bool→Bool` 枚举所有函数，证明共有 `2^2=4` 个；说明加 bottom 后数量和连续性条件如何变化。

证明要明确量化的是所有程序、所有上下文还是本脚本的有限样本；三者不能混写。

## Harness / LLM 工程联系

一个 tool schema 的类型解释是所有满足契约的值集合；函数 schema 还需要行为约束，单靠 JSON 形状无法刻画。

## 严格 60 分钟

| 分钟 | 动作 |
|---:|---|
| 0–5 | 闭卷回答入口问题 |
| 5–25 | 精读两段材料并回答问题 |
| 25–38 | 完成推导/证明 |
| 38–55 | 运行及改造 `practice.py` |
| 55–60 | 对照验收并记录模型边界 |

合计严格为 60 分钟。

## 验收

- [ ] 正确枚举 Bool、有限 Nat 和函数空间。
- [ ] 非法输出映射不属于箭头类型解释。
- [ ] 动手改造：加入积类型并验证基数乘法。

## 可选延伸（不计入 60 分钟）

阅读 Pitts §3.3 function domain construction 复习连续性。
