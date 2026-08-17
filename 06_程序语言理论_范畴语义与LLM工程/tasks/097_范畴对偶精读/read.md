# 第 097 晚：对偶原理与表示无关的定义

## 具体目标

- 构造有限范畴的 opposite。
- 验证 identity/associativity 在反向后保持。
- 检查 initial↔terminal、product↔coproduct 的陈述变换。

## 前置编号

- 必须完成：092–096
- 入口问题：把一个定理对偶化时，哪些词需要成对替换？

## 必读（20 分钟，已计入总时长）

| 分钟 | 开放权威一手材料与版本 | 精确讲次/章节/页内标题 | 阅读问题 |
|---:|---|---|---|
| 5–15 | [Emily Riehl, Category Theory in Context（作者开放版）](https://emilyriehl.github.io/files/context.pdf) | §1.2 “Duality” 全节，重点 opposite category 与 principle of duality | 为什么从范畴公理可机械得到所有对偶定理？ |
| 15–25 | [Cambridge Category Theory 2023–24 合并讲义](https://www.cl.cam.ac.uk/teaching/2324/CAT/CATLectureNotes.pdf) | Lecture 3 的 opposite/initial 部分与 Lecture 4 的 product/coproduct 对偶 | 证明 coproduct 定理时如何复用 product 的证明而不重做元素计算？ |

只读指定讲次或小节；练习题不自动算入必读。

## 导读

对偶不是交换词汇的比喻，而是反转所有箭头及复合顺序。任何只用范畴语言表述和证明的定理，都有自动的对偶版本。

## 必做推导 / 证明

从 terminal objects unique up to unique isomorphism 的证明逐箭头反向，得到 initial objects 的版本。

交换图必须标出对象、箭头方向与复合顺序；只画无标签三角形不合格。

## Harness / LLM 工程联系

producer/consumer、request/result 在工程图中经常方向相反，但只有当全部结构和定律都同步反向时才是真正数学对偶。这个检查可防止滥用术语。

范畴论在此提供定律和组合语言；除代码或 Cordis 论文明确使用外，不声称 Harness 内部直接运行范畴结构。

## 严格 60 分钟

| 时间 | 工作 |
|---:|---|
| 0–5 | 闭卷回答入口问题并画一个最小例子 |
| 5–25 | 完成两段精读与阅读问题 |
| 25–38 | 完成交换图/泛性质证明 |
| 38–55 | 运行并改造 `practice.py` |
| 55–60 | 验收并写一条 category law |

5 + 20 + 13 + 17 + 5 = 60 分钟。

## 验收

- [ ] opposite 的两次应用恢复原范畴。
- [ ] 始末对象搜索结果交换。
- [ ] 动手改造：自动替换一个小型 diagram 的全部箭头。

## 可选延伸（不计入 60 分钟）

阅读 Riehl §1.2 后列出 mono/epi 的对偶，但不深入证明。

