# 第 094 晚：始对象、末对象、对偶与自由幺半群

## 具体目标

- 搜索有限 preorder category 的始末对象。
- 构造 opposite 并验证始末互换。
- 实现自由幺半群到任意幺半群的唯一延拓。

## 前置编号

- 必须完成：092–093
- 入口问题：“存在唯一箭头”中的唯一性为何比仅存在更强？

## 必读（20 分钟，已计入总时长）

| 分钟 | 开放权威一手材料与版本 | 精确讲次/章节/页内标题 | 阅读问题 |
|---:|---|---|---|
| 5–15 | [Cambridge Category Theory 2023–24 合并讲义](https://www.cl.cam.ac.uk/teaching/2324/CAT/CATLectureNotes.pdf) | Lecture 3 “Terminal objects, opposite categories, initial objects, free monoids” | 在 opposite category 中 terminal object 变成什么？ |
| 15–25 | [Emily Riehl, Category Theory in Context（作者开放版）](https://emilyriehl.github.io/files/context.pdf) | Riehl §§1.2 “Duality” 与 2.3 “Universal properties” 中 initial/terminal examples | 泛性质如何只凭箭头刻画对象而不提内部表示？ |

只读指定讲次或小节；练习题不自动算入必读。

## 导读

始末对象由从/到所有对象的唯一箭头刻画，因此在同构意义下唯一。自由幺半群的 universal map 由生成元映射唯一决定，实际就是 fold。

## 必做推导 / 证明

证明两个 terminal objects 之间存在唯一同构；分别构造两个方向箭头并用唯一性证明复合为 identity。

交换图必须标出对象、箭头方向与复合顺序；只画无标签三角形不合格。

## Harness / LLM 工程联系

唯一扩展性质适合解释“只提供生成器/配置片段，系统唯一组合出完整解释”。它比某个具体列表实现更稳定。

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

- [ ] 脚本识别 chain 的 initial/terminal。
- [ ] opposite 后两者交换。
- [ ] 动手改造：以整数加法 monoid 验证 word fold 的同态律。

## 可选延伸（不计入 60 分钟）

阅读 Riehl §2.3 的 representable formulation。

