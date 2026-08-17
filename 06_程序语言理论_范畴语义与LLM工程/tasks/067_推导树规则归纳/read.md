# 第 067 晚：归纳定义与规则归纳

## 具体目标

- 把 big-step judgement 表示成带规则名的 derivation tree。
- 局部检查每条规则的前提和结论。
- 用规则归纳证明求值结果为整数。

## 前置编号

- 必须完成：064、066
- 入口检查：结构归纳研究语法树；规则归纳的研究对象是什么？

## 必读表（20 分钟，计入总计）

| 分钟 | 开放权威材料及版本 | 精确章节/页码/页内标题 | 阅读问题 |
|---:|---|---|---|
| 5–15 | [Cambridge, Semantics of Programming Languages 2025–26 官方讲义](https://www.cl.cam.ac.uk/teaching/2526/Semantics/notes.pdf) | §3.2 “Inductive definitions and rule induction” pp.41–46 | rule induction 的归纳假设对应推导树中的哪些前提？ |
| 15–25 | [Software Foundations LF 7.0，IndProp](https://softwarefoundations.cis.upenn.edu/lf-current/IndProp.html) | “Inductively Defined Propositions” 与 “Using Evidence in Proofs” | 为何对 derivation evidence 分析比对终点表达式分类更直接？ |

材料均来自大学官方课程或教材官方站点；PDF 页码以讲义印刷页码为准。

## 导读

一个 judgement 成立是因为存在有限推导。规则归纳按最后使用的规则分类，并为每个子推导提供归纳假设。可检查推导树比只返回答案包含更多证据。

## 今晚推导 / 证明

对加法 big-step 推导证明：若 `e ⇓ v`，则 `v` 是整数。明确 `E_Num` 与 `E_Add` 两个分支。

推导必须写出配置、规则名与规则前提；只写最终值不合格。

## Harness / LLM 联系

工具执行 trace 若记录 producer、输入和输出，就能像 derivation evidence 一样离线验证。只存最终响应会丢失支撑审计的中间前提。

## 严格 60 分钟

| 时段 | 任务 | 输出 |
|---:|---|---|
| 0–5 | 闭卷回答入口问题 | 定义和一个反例 |
| 5–25 | 按必读表精读 | 两个问题各 2–3 句 |
| 25–38 | 完成推导/证明 | 可检查的规则树或归纳步骤 |
| 38–55 | 运行并改造 `practice.py` | 正反/边界断言全通过 |
| 55–60 | 按验收清单复盘 | 一条不变量和一个疑问 |

合计 5 + 20 + 13 + 17 + 5 = 60 分钟。

## 验收

- [ ] 能解释结构归纳与规则归纳的不同对象。
- [ ] 脚本接受合法推导，拒绝伪造结论和缺失前提。
- [ ] 动手改造：加入变量环境规则。

## 可选延伸（不计入 60 分钟）

阅读 LF `IndProp` 中关系的反演示例。

