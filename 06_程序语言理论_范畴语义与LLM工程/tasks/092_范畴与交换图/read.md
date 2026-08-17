# 第 092 晚：范畴、复合与交换图

## 具体目标

- 表示对象、带端点箭头和部分复合。
- 检查单位律、结合律与 closure。
- 用两条路径的复合相等验证交换图。

## 前置编号

- 必须完成：第 3 周代数结构及 071–084 语义
- 入口问题：范畴公理对对象集合本身施加了什么运算？

## 必读（20 分钟，已计入总时长）

| 分钟 | 开放权威一手材料与版本 | 精确讲次/章节/页内标题 | 阅读问题 |
|---:|---|---|---|
| 5–15 | [Cambridge Category Theory 2023–24 合并讲义](https://www.cl.cam.ac.uk/teaching/2324/CAT/CATLectureNotes.pdf) | Lecture 1 “Categories, Set, diagrams”：definition of category、identity、associativity | 复合的可定义条件如何由 domain/codomain 决定？ |
| 15–25 | [Emily Riehl, Category Theory in Context（作者开放版）](https://emilyriehl.github.io/files/context.pdf) | Riehl §1.1 “Abstract and concrete categories”，Definitions 1.1.1–1.1.4 | 小范畴、局部小范畴和具体范畴分别增加什么条件？ |

只读指定讲次或小节；练习题不自动算入必读。

## 导读

范畴只要求可复合箭头的结合律和每个对象的恒等箭头。复合是部分定义的：只有前箭头 codomain 等于后箭头 domain 才能复合。交换图是多条合法路径复合相等。

## 必做推导 / 证明

写出三个可复合箭头 `f:A→B,g:B→C,h:C→D` 的结合律两边；再画自然数偏序 `0≤1≤2` 的交换三角形。

交换图必须标出对象、箭头方向与复合顺序；只画无标签三角形不合格。

## Harness / LLM 工程联系

插件服务之间的合法组合可用对象/箭头抽象，结合律意味着括号重排不改变组合结果。但真实副作用需额外的 effect 结构，不能仅靠范畴公理。

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

- [ ] checker 验证 identity、closure、associativity。
- [ ] 删除一个 composite 后负例被拒绝。
- [ ] 动手改造：加入离散范畴生成器。

## 可选延伸（不计入 60 分钟）

阅读 Riehl §1.1 中 group、groupoid 和 preorder 示例。

