# 第 17 晚：cut LP、moat growing 与 Steiner 网络

## 目标

理解网络设计的 cut relaxation 与“壕沟增长”；以 metric-closure MST 实现 Steiner Tree 2-近似；看清该算法和 primal-dual 2-近似的共同收费结构。

## 前置回忆（5 分钟）

Steiner Tree 给图 `G=(V,E)` 与 terminals `R`，可使用非终端 Steiner 点连通 R。对任何把终端分开的 cut `δ(S)`，整数解至少取几条跨边？

## 精读正文（20 分钟）

cut LP 写作 `min Σ_ec_ex_e`，对每个 `S` 满足 `S∩R≠∅` 且 `R\S≠∅`，有 `Σ_{e∈δ(S)}x_e>=1`。对偶给每个有效 cut/moat 变量，边容量约束为“穿过它的 moat 总增长不超过 c_e”。primal-dual 算法同时增长活跃连通分量的 moat，边 tight 时合并，再 prune；每条最终树边两侧收费，导致约 2 的分析。

本晚代码实现等价但更易自包含的 metric-closure 版本：先求原图全点对最短路；在终端度量上求 MST；把 MST 边展开回原图路径并取并集。证明：把最优 Steiner 树每边复制两次得 Euler 游，shortcut 到终端 tour 成本 `<=2OPT`；终端 MST 不超过该 tour，展开不改变成本，取并集只会更便宜。因此 ALG `<=2OPT`。

这里终端 MST 与原图“只在终端诱导子图做 MST”不同：后者可能断开或极贵，必须允许最短路径经过 Steiner 点。一般 Steiner Tree 的最佳已知多项式近似优于 1.39，而经典 2 只是入口；代码的精确 oracle 枚举边子集并检查终端连通，仅适合很小图。

## 精确 60 分钟

- 00–05：写 cut 约束。
- 05–25：画 moat 增长与 edge tight；复现 doubled-tree 证明。
- 25–45：运行最短路+终端 MST+路径展开。
- 45–55：构造终端诱导 MST 失败的例子。
- 55–60：说出 metric closure 的必要性。

## 代码实验

脚本随机小图，Floyd–Warshall 保存路径，终端 Kruskal 后展开；枚举边子集求 OPT 并断言 `ALG<=2OPT`。

## 验收

- 能写有效 cut 的条件。
- 能解释每边复制两次的 2 从何而来。
- 能区分 metric closure 与终端诱导子图。

## 原始/权威资料

- Goemans & Williamson (1995), primal-dual network design: <https://doi.org/10.1007/BF01585996>
- Byrka et al. (2013), An improved LP-based approximation for Steiner Tree: <https://doi.org/10.1145/2492007.2492022>

