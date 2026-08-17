# 第 25 晚：在线优化、竞争比与随机 Ranking

## 学习目标

- 区分离线最优、在线策略、到达模型与对手能力。
- 用 competitive ratio 评价逐步决策而非单一分布平均。
- 理解在线二分匹配 Ranking 算法的随机化位置。
- 小规模精确枚举到达序和随机 rank，避免采样误读。

## 前置回忆

在线二分匹配中，离线侧及边可预先给定或随着在线点到达揭示；在线点一到必须立即匹配某个空闲邻居或放弃，决定不可撤销。

## 完整精读讲解

最大化在线算法若对所有输入序列满足 $ALG(\sigma)\ge\alpha OPT(\sigma)-\beta$，称竞争比至少 $\alpha$（忽略/声明加性常数）。必须说明 adversary：oblivious adversary 在随机种子抽取前固定序列；adaptive adversary 可观察行为，随机保证可能改变。

朴素 deterministic greedy 对在线二分匹配有 1/2 保证且该界可紧。Karp–Vazirani–Vazirani 的 Ranking 在开始时给每个离线点独立随机 rank；在线点到达时匹配可用邻居中 rank 最优者。对任意由 oblivious adversary 固定的到达序，其期望匹配大小至少 $(1-1/e)OPT$，并且该常数是经典模型中的最优界。

随机性作用在离线点优先级，而非假设到达随机。小实例可枚举所有 rank 排列精确算期望，再对所有到达排列找最坏值；这比几十次 Monte Carlo 更能暴露量词顺序：先固定输入，再对算法随机性取期望，最后取最坏输入。

在线学习/优化还有 regret 视角，与事后最佳固定动作比较；它和 competitive analysis 的 benchmark 不同。resource augmentation、随机到达、已知分布会给不同可能性。陷阱：用平均随机到达结果声称 adversarial guarantee、让 adversary 看到随机 rank、比较不同信息模型、离线 OPT 算错、只报 ratio 不报绝对规模。

## 精确 60 分钟

- 00–07：写清信息揭示与不可撤销动作。
- 07–18：构造 deterministic greedy 的 1/2 例。
- 18–30：追踪 Ranking 的一次到达。
- 30–39：理解期望与最坏序的量词顺序。
- 39–53：枚举 rank/arrival，算精确分数。
- 53–58：改变图并找最差到达序。
- 58–60：区分 competitive ratio 与 regret。

## 代码任务

实现 Ranking；枚举所有离线 rank 和在线 arrival permutation，求每个 arrival 下期望匹配，再与离线最大匹配比较并报告最坏 ratio。

## 验收标准

- 每个点至多匹配一次且边存在。
- 期望用精确 Fraction 而非少量抽样。
- benchmark 是同一图的离线最大匹配。
- 明确保证针对 oblivious adversary。

## 原始/权威资料

- Karp, Vazirani & Vazirani 1990 Ranking：https://doi.org/10.1145/100216.100262
- Borodin & El-Yaniv, Online Computation and Competitive Analysis：https://www.cambridge.org/core/books/online-computation-and-competitive-analysis/6CF74D6B75D38FF6E5F169DAAFB71000
- Mehta 2013 Online Matching survey：https://doi.org/10.1561/0400000057
