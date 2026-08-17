# 第 074 晚：CPO、ω 链与 Scott 连续性

## 具体目标

- 在有限 powerset CPO 上表示链与 supremum。
- 检查链性、最小上界和连续性方程。
- 解释有限模型为何只能作为定理的实验。

## 前置编号

- 必须完成：073
- 入口问题：单调为何不足以直接说明函数保持无限近似的极限？

## 必读（20 分钟，计入 60 分钟）

| 分钟 | 开放权威一手材料与版本 | 精确页码与章节 | 阅读问题 |
|---:|---|---|---|
| 5–15 | [Andrew M. Pitts, Denotational Semantics（Cambridge 官方讲义）](https://www.cl.cam.ac.uk/teaching/1112/DenotSem/dens-notes-bw.pdf) | §2.3 “Complete partial orders and continuous functions” pp.19–27 | CPO 要求哪些链有上确界，而非要求所有子集有什么？ |
| 15–25 | [Andrew M. Pitts, Denotational Semantics（Cambridge 官方讲义）](https://www.cl.cam.ac.uk/teaching/1112/DenotSem/dens-notes-bw.pdf) | §2.3 中 continuous function 定义、链上确界保持式及函数空间 | Scott 连续性如何交换函数应用与链上确界？ |

版本固定为 Pitts 的 Cambridge 2011–12 课程讲义发布版；页码采用正文印刷页码。到点停止，不把后续章节算作“已经读过”。

## 导读

CPO 为逐步增加的信息链提供极限。连续函数既单调，又保持链的上确界。有限格中的链最终稳定，因此实验会掩盖无限情形的难点，read.md 的推导必须处理一般定义。

## 必做推导 / 证明

证明 powerset 格中递增链的上确界是并集；对 `F(X)=X∪{a}` 验证 `F(⋃Xi)=⋃F(Xi)`。

必须写出序、函数空间或不动点中的对象类型；不能把数学上的 bottom 与 Python 的偶然异常混为一谈。

## Harness / LLM 工程联系

流式生成前缀形成信息增长链；稳定的 projection 理想上应保持前缀极限。不过真实 token 流和取消语义还需要额外建模。

这里只使用组合性、近似和不动点作为分析工具，不声称 Harness 以该指称模型实现。

## 严格 60 分钟

| 时段 | 动作 |
|---:|---|
| 0–5 | 闭卷写入口问题的定义与反例 |
| 5–25 | 完成两段精读和阅读问题 |
| 25–38 | 手算本晚推导/证明 |
| 38–55 | 运行并按顶部说明改造 `practice.py` |
| 55–60 | 完成验收，写一条不变量 |

总计 5 + 20 + 13 + 17 + 5 = 60 分钟。

## 验收

- [ ] 能区别 complete lattice 与 CPO。
- [ ] 脚本验证合法链、supremum 和连续性方程。
- [ ] 动手改造：加入一个非链集合并说明为何不能套用公式。

## 可选延伸（不计入 60 分钟）

阅读 Pitts pp.27–28 的 admissible properties 铺垫。
