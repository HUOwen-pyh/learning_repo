# 第 096 晚：指数对象与笛卡尔闭范畴

## 具体目标

- 枚举有限函数对象 `B^A`。
- 实现 eval、curry、uncurry。
- 验证 β/η 方程和 hom-set 基数。

## 前置编号

- 必须完成：095 与 057 Curry–Howard
- 入口问题：Set 中 `B^A` 的元素是什么，evaluation map 的类型是什么？

## 必读（20 分钟，已计入总时长）

| 分钟 | 开放权威一手材料与版本 | 精确讲次/章节/页内标题 | 阅读问题 |
|---:|---|---|---|
| 5–15 | [Cambridge Category Theory 2023–24 合并讲义](https://www.cl.cam.ac.uk/teaching/2324/CAT/CATLectureNotes.pdf) | Lecture 5 “Exponentials and cartesian closed categories” | curry/uncurry 的自然双射连接哪两个 hom-set？ |
| 15–25 | [Steve Awodey, Categorical Logic 讲义第 4 章（作者开放版）](https://awodey.github.io/catlog/notes/catlog4.pdf) | §4.2 “Cartesian Closed Categories”，定义 4.2.1 与 evaluation/currying 方程 | 指数对象为何是函数类型的范畴语义？ |

只读指定讲次或小节；练习题不自动算入必读。

## 导读

指数对象把从 product 出发的二元映射内部化为普通箭头。CCC 同时具有 terminal、binary products 和 exponentials，是 STLC 的核心语义环境。

## 必做推导 / 证明

写出 `Hom(C×A,B) ≅ Hom(C,B^A)` 两个方向，并证明 curry/uncurry 互逆。

交换图必须标出对象、箭头方向与复合顺序；只画无标签三角形不合格。

## Harness / LLM 工程联系

高阶工具组合器把上下文 C 与输入 A 的处理逻辑封装成可传递的函数对象。βη 律提供内联/封装不改变行为的重构准则。

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

- [ ] 函数对象基数等于 `|B|^|A|`。
- [ ] curry/uncurry 对所有有限输入互逆。
- [ ] 动手改造：加入空 A，解释为何 `B^0` 是 singleton。

## 可选延伸（不计入 60 分钟）

预读 Cambridge Lecture 7：STLC types in a CCC。
