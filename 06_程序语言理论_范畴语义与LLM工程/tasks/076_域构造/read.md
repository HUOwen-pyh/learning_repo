# 第 076 晚：域构造：平坦域、积域与函数域

## 具体目标

- 实现 bottom 提升的平坦域顺序。
- 实现 product pointwise order。
- 枚举有限函数并检查 pointwise monotonicity。

## 前置编号

- 必须完成：074–075
- 入口问题：函数域的序为什么按每个输入点逐点比较？

## 必读（20 分钟，计入 60 分钟）

| 分钟 | 开放权威一手材料与版本 | 精确页码与章节 | 阅读问题 |
|---:|---|---|---|
| 5–15 | [Andrew M. Pitts, Denotational Semantics（Cambridge 官方讲义）](https://www.cl.cam.ac.uk/teaching/1112/DenotSem/dens-notes-bw.pdf) | §3 “Domain constructions” pp.33–43；§3.1 flat domains pp.33–34 | flat domain 中不同非 bottom 值为何不可比？ |
| 15–25 | [Andrew M. Pitts, Denotational Semantics（Cambridge 官方讲义）](https://www.cl.cam.ac.uk/teaching/1112/DenotSem/dens-notes-bw.pdf) | §3.2 products pp.34–38 与 §3.3 function domains pp.38–43 | 积域和函数域分别怎样计算顺序与链上确界？ |

版本固定为 Pitts 的 Cambridge 2011–12 课程讲义发布版；页码采用正文印刷页码。到点停止，不把后续章节算作“已经读过”。

## 导读

复杂语义域从简单域组合而来。平坦域用 bottom 表示未定义；积按分量携带信息；函数按每个输入点比较输出信息。脚本只用有限载体，以便穷举法验证公理。

## 必做推导 / 证明

证明若 A、B 是偏序，则逐点定义的 `A×B` 也是偏序；反对称分支要显式用两个分量的反对称性。

必须写出序、函数空间或不动点中的对象类型；不能把数学上的 bottom 与 Python 的偶然异常混为一谈。

## Harness / LLM 工程联系

工具结果可看成 product domain：不同字段独立变得已知。流式 partial result 的合并必须按字段信息增长，不能把已知值悄悄退回 unknown。

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

- [ ] flat domain 只允许 bottom 小于普通值。
- [ ] product 和 finite function 的 pointwise order 断言通过。
- [ ] 动手改造：加入 lifted error，决定 error 与普通值是否可比。

## 可选延伸（不计入 60 分钟）

阅读 Pitts §4 Scott induction pp.45–52。
