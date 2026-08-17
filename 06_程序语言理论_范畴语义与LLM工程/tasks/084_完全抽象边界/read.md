# 第 084 晚：周验收：完全抽象及模型边界

## 具体目标

- 写出 full abstraction 的两个方向。
- 构造语义过细导致不 fully abstract 的有限反例。
- 解释可观察量选择会改变 contextual equivalence。

## 前置编号

- 必须完成：079、082–083
- 入口问题：fully abstract 模型要求 denotational equality 与哪一种程序等价完全重合？

## 必读表（20 分钟，计入总时长）

| 分钟 | 开放权威一手材料与版本 | 精确章节、页码或锚点 | 阅读问题 |
|---:|---|---|---|
| 5–15 | [Andrew M. Pitts, Denotational Semantics（Cambridge 官方讲义）](https://www.cl.cam.ac.uk/teaching/1112/DenotSem/dens-notes-bw.pdf) | Ch.8 “Full abstraction” pp.91–99 | soundness/adequacy 已有后，为何模型仍可能区分程序无法观察的细节？ |
| 15–25 | [Milner, Fully Abstract Models of Typed Lambda-Calculi](https://doi.org/10.1016/0304-0208(77)90053-6) | §1 full abstraction criterion 与 observational equivalence 定义 | “没有多区分、也没有少区分”如何写成双向蕴含？ |

Pitts PDF 固定为 Cambridge 2011–12 课程讲义发布版；网页采用当前公开章版。页码按正文印刷页，只读规定范围。

## 导读

完全抽象要求语义相等恰好等于上下文不可区分。模型过粗会把可区分程序合并，过细会保留语言无法观察的信息。脚本用只能观察奇偶性的玩具语言制造过细模型反例。

## 必做推导或证明

写 `⟦e⟧=⟦e'⟧ ⇔ e≈ctx e'`，分别给两个方向命名；对脚本的 0 和 2 说明右真左假。

证明要明确量化的是所有程序、所有上下文还是本脚本的有限样本；三者不能混写。

## Harness / LLM 工程联系

LLM eval 若记录隐藏实现细节，可能把用户不可观察差异当作失败；若指标过粗，又会合并任务状态不同的结果。full abstraction 提供校准评测粒度的语言。

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

- [ ] 能区分 sound、adequate、fully abstract。
- [ ] 脚本展示 exact-int 模型过细的 witness。
- [ ] 动手改造：加入 `isZero` 上下文并重新计算等价类。

## 可选延伸（不计入 60 分钟）

阅读 Pitts Ch.8 后写 150 字说明 PCF full abstraction 的历史难点。
