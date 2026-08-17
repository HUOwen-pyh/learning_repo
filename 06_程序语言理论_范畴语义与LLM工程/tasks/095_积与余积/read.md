# 第 095 晚：积、余积与泛映射

## 具体目标

- 用投影与唯一 pairing 验证 Set 中的积。
- 用注入与唯一 copairing 验证余积。
- 覆盖空集/初对象边界。

## 前置编号

- 必须完成：094
- 入口问题：笛卡尔积的泛性质量化的是元素，还是所有锥和箭头？

## 必读（20 分钟，已计入总时长）

| 分钟 | 开放权威一手材料与版本 | 精确讲次/章节/页内标题 | 阅读问题 |
|---:|---|---|---|
| 5–15 | [Cambridge Category Theory 2023–24 合并讲义](https://www.cl.cam.ac.uk/teaching/2324/CAT/CATLectureNotes.pdf) | Lecture 4 “Products and coproducts”：cones、projections/injections、unique mediating morphism | pairing `⟨f,g⟩` 的两个交换方程是什么？ |
| 15–25 | [Emily Riehl, Category Theory in Context（作者开放版）](https://emilyriehl.github.io/files/context.pdf) | Riehl §3.1 “Limits and colimits” 中 binary products/coproducts examples | 余积如何由 opposite category 中的积得到？ |

只读指定讲次或小节；练习题不自动算入必读。

## 导读

积不是仅指 pair 数据结构，而是满足对任意共同源锥存在唯一中介箭头的对象。余积把箭头全部反向。脚本在有限 Set 中通过穷举函数验证方程和唯一性。

## 必做推导 / 证明

给 `f:X→A,g:X→B` 构造唯一 `u:X→A×B`；证明任何满足两个投影方程的 v 都逐点等于 u。

交换图必须标出对象、箭头方向与复合顺序；只画无标签三角形不合格。

## Harness / LLM 工程联系

把两项独立服务结果组合为 product，需要所有消费者都能通过投影恢复原结果；tagged union 对应 coproduct，可由 case handler 唯一解释。

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

- [ ] pair/copaired maps 满足两侧交换方程。
- [ ] 脚本确认有限候选中 mediator 唯一。
- [ ] 动手改造：加入三元积并用二元积结合。

## 可选延伸（不计入 60 分钟）

证明 `(A×B)×C ≅ A×(B×C)` 而非宣称二者字面相等。

