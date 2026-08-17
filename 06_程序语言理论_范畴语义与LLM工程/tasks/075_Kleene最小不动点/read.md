# 第 075 晚：Kleene 链与最小不动点定理

## 具体目标

- 实现从 bottom 开始的 Kleene iteration。
- 检测稳定点并验证它是最小前不动点。
- 用可达闭包解释迭代语义。

## 前置编号

- 必须完成：073–074
- 入口问题：为什么从 bottom 开始，而不是任意点开始迭代？

## 必读（20 分钟，计入 60 分钟）

| 分钟 | 开放权威一手材料与版本 | 精确页码与章节 | 阅读问题 |
|---:|---|---|---|
| 5–15 | [Andrew M. Pitts, Denotational Semantics（Cambridge 官方讲义）](https://www.cl.cam.ac.uk/teaching/1112/DenotSem/dens-notes-bw.pdf) | §2.4 “Tarski's fixed point theorem” pp.29–31 | 连续函数的最小不动点由哪条 ω 链的上确界给出？ |
| 15–25 | [Andrew M. Pitts, Denotational Semantics（Cambridge 官方讲义）](https://www.cl.cam.ac.uk/teaching/1112/DenotSem/dens-notes-bw.pdf) | §2.4 定理证明中 monotonicity、continuity 与 leastness 三个步骤 | 证明最小性时如何归纳得到每个近似都不超过任意 pre-fixed point？ |

版本固定为 Pitts 的 Cambridge 2011–12 课程讲义发布版；页码采用正文印刷页码。到点停止，不把后续章节算作“已经读过”。

## 导读

Kleene 构造把递归定义转换成一列有限信息：⊥、F⊥、F²⊥……连续性允许在极限处交换 F 与上确界，归纳则给出最小性。

## 必做推导 / 证明

完整证明：若 `F(a)≤a`，则对所有 n 有 `F^n(⊥)≤a`；由此推出链上确界不超过 a。

必须写出序、函数空间或不动点中的对象类型；不能把数学上的 bottom 与 Python 的偶然异常混为一谈。

## Harness / LLM 工程联系

多轮工具规划的有限深度结果可按迭代层组织。固定点视角能区分“尚未探索到”与“已闭包稳定”，适合依赖发现和数据流分析。

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

- [ ] 脚本输出从空集到可达闭包的严格增长链。
- [ ] 最终集合满足 fixed point 且不遗漏 reachable 节点。
- [ ] 动手改造：加入不可达环并验证不进入最小不动点。

## 可选延伸（不计入 60 分钟）

比较 worklist 与朴素全量迭代，只测操作次数。
