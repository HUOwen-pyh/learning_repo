# 第 26 晚：一次扫描、有限内存与可证明摘要

## 目标

理解 streaming 模型的空间/遍数/失败概率；实现 Count-Min Sketch；实现带 OPT 猜测的单阈值流式子模 1/2 内核，并知道如何用几何猜测消除 oracle。

## 前置回忆（5 分钟）

数据流中频率向量 `f∈N^U`，point query 要估 `f_x`。若把多个 key 哈希到同一桶，为什么只会高估？第 24 晚的边际收益为何随已选集合增大而下降？

## 精读正文（20 分钟）

Count-Min 用 d 行、w 桶；每行独立哈希，更新 key 时对应桶加增量，查询取各行最小。非负 turnstile/插入流中永不低估。固定 key 在一行的碰撞噪声期望至多 `N/w`，取 `w≈e/ε` 后 Markov 给常数失败率；d 行取最小把失败率降到 `δ`，空间 `O(ε^{-1}log(1/δ))`，与 universe 大小无关。保证通常是 `estimate<=f_x+ε||f||_1`，且量词可能只对固定 query，不自动同时覆盖所有自适应查询。

流式单调次模：若知道 `v=OPT`，一次扫描中当元素边际至少 `v/(2k)` 且尚未满 k 就接纳。若选满，值至少 v/2；若未满，每个被拒绝的最优元素在到达时边际小于阈值，次模性使其最终边际更小，故 `OPT<=f(S)+k·v/(2k)`，得到 `f(S)>=OPT/2`。未知 OPT 时并行维护几何猜测 `v∈{(1+ε)^i}`，范围由当前最大 singleton 与 k 倍它界定，得到 `1/2-O(ε)`、`O(k log k/ε)` 级存储的 Sieve-Streaming 思路。

代码分别验证 sketch 不低估与流式阈值的 1/2。它把精确 OPT 仅作为“正确猜测 oracle”；动手改造才实现并行猜测。删除流/负更新不能直接用 Count-Min 的单侧保证。

## 精确 60 分钟

- 00–05：写 sketch 三个资源指标。
- 05–25：推 Count-Min 噪声和流式 1/2 两个证明。
- 25–45：运行随机数据流与随机到达覆盖实例。
- 45–55：实现 `(1+ε)` 并行猜测。
- 55–60：说明 fixed-query 与 for-all 保证差别。

## 代码实验

同一脚本先对频率流做 sketch/exact 对拍，再对 max coverage 随机顺序做 threshold stream/exact OPT 对拍；两部分都固定随机种子。

## 验收

- 能写 Count-Min 的加性误差尺度。
- 能完成流式 1/2 的“满/不满”分类证明。
- 能解释正确 OPT 猜测如何被几何网格替代。

## 原始/权威资料

- Cormode & Muthukrishnan (2005), An improved data stream summary: <https://doi.org/10.1016/j.jalgor.2003.12.001>
- Badanidiyuru et al. (2014), Streaming submodular maximization: <https://doi.org/10.1145/2623330.2623637>
