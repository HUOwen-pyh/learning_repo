# 第 093 晚：偏序与幺半群作为范畴

## 具体目标

- 从有限偏序生成 thin category。
- 从幺半群生成单对象范畴。
- 把范畴单位律/结合律还原成幺半群律。

## 前置编号

- 必须完成：092 与 050–056
- 入口问题：为什么 thin category 的每对对象之间至多一条箭头？

## 必读（20 分钟，已计入总时长）

| 分钟 | 开放权威一手材料与版本 | 精确讲次/章节/页内标题 | 阅读问题 |
|---:|---|---|---|
| 5–15 | [Cambridge Category Theory 2023–24 合并讲义](https://www.cl.cam.ac.uk/teaching/2324/CAT/CATLectureNotes.pdf) | Lecture 2 “Preorders, monoids and monoid homomorphisms as categories” | 偏序的反对称性是否是形成范畴所必需？ |
| 15–25 | [Emily Riehl, Category Theory in Context（作者开放版）](https://emilyriehl.github.io/files/context.pdf) | Riehl §1.1 中 preorders 与 one-object categories 示例 | 单对象范畴的 identity 和 composition 对应幺半群的哪些数据？ |

只读指定讲次或小节；练习题不自动算入必读。

## 导读

preorder 把 `x≤y` 视作唯一可能箭头；monoid 则把所有元素视作同一对象上的 endomorphism。两种编码展示对象少或 hom-set 薄时，范畴公理退化为熟悉代数律。

## 必做推导 / 证明

证明 one-object category 给出 monoid，反向构造也成立；明确单位元和乘法对应关系。

交换图必须标出对象、箭头方向与复合顺序；只画无标签三角形不合格。

## Harness / LLM 工程联系

日志 patch、配置变换若具有结合组合和空操作，就形成 monoid；将其看成单对象范畴便于随后理解 functor 和 monad，但不自动保证副作用可逆。

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

- [ ] 脚本生成并检查 preorder category。
- [ ] 模 3 加法 monoid category 满足全部 law。
- [ ] 动手改造：使用字符串自由幺半群的有限样本。

## 可选延伸（不计入 60 分钟）

构造只有 preorder 而非 partial order 的两个等价对象例子。

