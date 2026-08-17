# 第 057 晚：Curry–Howard：证明即程序

## 具体目标

- 把原子命题、蕴含和合取表示成类型。
- 实现 proof term 的类型检查器。
- 从一个程序读出定理，并从自然演绎构造程序。

## 前置编号

- 必须完成：050、053、056
- 闭卷入口问题：蕴含引入和 lambda 抽象为什么是同一条规则的两种读法？

## 必读（20 分钟，已计入 60 分钟）

| 分钟 | 开放权威一手材料与版本 | 精确章节、页码或页内标题 | 阅读问题 |
|---:|---|---|---|
| 5–15 | [Cambridge Topics in Type Systems 2024–25](https://www.cl.cam.ac.uk/teaching/2425/Types/materials.html) | Lecture 2 “The Curry–Howard correspondence”，natural deduction、proof terms 与 implication fragment | 一个 typing derivation 如何同时成为命题证明？ |
| 15–25 | [Software Foundations LF 7.0，ProofObjects](https://softwarefoundations.cis.upenn.edu/lf-current/ProofObjects.html) | “Proof Scripts and Proof Objects” 至 “Logical Connectives as Inductive Types” | Coq 检查 proof object 时真正信任的核心是什么？ |

只读指定边界；链接均为大学官方讲义、作者版本或正式论文页面。

## 导读

Curry–Howard 不是相似性口号，而是规则逐项对应：假设是变量，蕴含引入是 lambda，蕴含消去是应用，合取引入是 pair。今晚只处理直觉主义命题片段，以便每个证明都能执行和检查。

## 必做推导 / 证明

构造并检查 `(A→B)→(B→C)→A→C` 的 proof term；再为 `A∧B→B∧A` 写完整推导树。

必须保留判断形式和规则名；“凭直觉显然”不算完成。

## DeepSeek Harness / LLM 工程联系

工具组合器的类型可以被读成“若有前置能力 A，就产生结果 B”。类型检查后的组合相当于证明所需能力足以完成工作，而不是靠运行时碰运气。

这是从形式概念到工程约束的映射；除明确指出外，不宣称 Harness 已静态证明这些性质。

## 严格 60 分钟

| 时间 | 工作 |
|---:|---|
| 0–5 | 回忆入口问题，写定义和反例 |
| 5–25 | 完成必读表并回答两个问题 |
| 25–38 | 手写推导或证明 |
| 38–55 | 运行 `practice.py`，再完成文件顶部的动手改造 |
| 55–60 | 按验收项自测并记录一个疑问 |

5 + 20 + 13 + 17 + 5 = 60 分钟。下面的延伸不得挤入本晚。

## 验收

- [ ] 能逐条对应四个自然演绎规则与 term constructor。
- [ ] 脚本拒绝错误应用和未绑定假设。
- [ ] 动手改造：加入和类型，对应析取及 case elimination。

## 可选延伸（不计时）

阅读 SF `ProofObjects` 的 existential quantification 证明对象。

