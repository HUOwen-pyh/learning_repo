# 第 098 晚：周验收：有限范畴与泛性质检查器

## 具体目标

- 实现 finite poset category 的 category-law 检查。
- 搜索 initial、terminal、binary product 与 coproduct。
- 用缺失 meet/join 的负例检验 checker。

## 前置编号

- 必须完成：092–097
- 入口问题：在 thin category 中，为何 product 等价于 greatest lower bound？

## 必读（20 分钟，已计入总时长）

| 分钟 | 开放权威一手材料与版本 | 精确讲次/章节/页内标题 | 阅读问题 |
|---:|---|---|---|
| 5–15 | [Cambridge Category Theory 2023–24 合并讲义](https://www.cl.cam.ac.uk/teaching/2324/CAT/CATLectureNotes.pdf) | Lectures 1–5 总结：category laws、initial/terminal、products/coproducts、exponentials | 每个泛性质的 existence 与 uniqueness 应分别怎样由 checker 验证？ |
| 15–25 | [Emily Riehl, Category Theory in Context（作者开放版）](https://emilyriehl.github.io/files/context.pdf) | §2.3 “Universal properties” 与 §3.1 “Limits and colimits” 的 binary examples | 为何有限穷举 checker 的成功不构成任意范畴中的一般证明？ |

只读指定讲次或小节；练习题不自动算入必读。

## 导读

thin category 中 hom-set 至多一个，因而中介箭头唯一性自动化，product/coproduct 分别退化为最大下界/最小上界。周验收把前六晚的抽象定义转成可执行搜索。

## 必做推导 / 证明

证明在 preorder category 中，P 是 A、B 的 categorical product 当且仅当 P 是它们的 greatest lower bound。

交换图必须标出对象、箭头方向与复合顺序；只画无标签三角形不合格。

## Harness / LLM 工程联系

对服务依赖图做有限搜索可发现公共依赖或汇合点，但真实插件类别可能有多条不同 morphism，不能把所有工程图都简化为 poset。

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

- [ ] diamond lattice 的 initial/terminal 与 meet/join 全部正确。
- [ ] 非格 poset 的缺失 product 返回 None。
- [ ] 动手改造：返回 universal-property 失败 witness，而非布尔值。

## 可选延伸（不计入 60 分钟）

把 finite checker 扩为一般 hom-set category，并真正检查 mediator uniqueness。

