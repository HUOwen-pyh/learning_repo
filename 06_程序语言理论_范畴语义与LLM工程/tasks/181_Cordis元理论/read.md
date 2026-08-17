# 第181晚：Cordis 论文——元理论

## 目标与前置

- 目标：读懂 preservation、temporal/spatial composability、progress、confluence 的准确前提与结论。
- 前置：第177–180晚、不变量证明、偏序、终止、局部交换。

## 计入 60 分钟的必读

| 分钟 | 材料 | 版本 | 精确范围 | 问题 |
|---:|---|---|---|---|
| 38 | [Cordis paper](https://github.com/cordiverse/paper/blob/948a07b369c62adb3b12e102458be5c18dfb69b9/paper.pdf) | 948a07b369c62adb3b12e102458be5c18dfb69b9 | path paper.pdf；§4.4.1–§4.4.5，Theorems 59、61、63、64、66、73 及其直接引理，PDF pp.38–53；checked_at 2026-08-15 | 每个结论需要 independence、acyclicity、totality 或 quiescence 中哪些前提？ |

## 阅读导引

建表：定理号、性质、前提、结论、失去一个前提的反例。不要一次啃全部证明细节；精读 statement 和 proof spine，标出 Lemma 71 transposition、Lemma 72 deletion 如何支撑 confluence。

## 核心推导

preservation 证明良构状态对一步转移封闭；progress 排除满足前提时的永久停滞；confluence 说明允许的不同交错在静止点达到等价结果。confluence 不是“执行顺序毫无影响”，而是带 independence、acyclicity 等条件的结果。

## 工业联系与事实标签

- [THEOREM] 论文 Theorem 59 是 preservation；61 recovery exactness；63 ordering；64 resolution coherence；66 progress；73 confluence。课程不删减它们的原文假设。
- [EMPIRICAL] 这些是预印本中的证明主张，论文 README 明示仍在 active revision。
- [INFERENCE] 工业插件审计应把依赖环、不可逆 effect 和非 total provision 标为破坏证明前提的风险。
- [OPEN] 形式模型到具体 Cordis/Node 实现的 refinement proof 并未由运行测试替代。

## 严格 60 分钟

- 0–5：建前提表；5–43：精读 statements/proof spine；43–55：穷举有限交错；55–58：构造依赖环；58–60：写结论边界。

## 验收

能为六个主定理各说一个关键前提；代码验证独立操作交换和冲突反例；不把 confluence 当无条件确定性。

## 可选延伸

完整复核 Theorem 73 证明每一步，不计时。
