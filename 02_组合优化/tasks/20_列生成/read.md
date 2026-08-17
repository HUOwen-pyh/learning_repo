# 第 20 晚：Dantzig–Wolfe、列生成与切割库存

## 学习目标

- 理解变量指数多时为何按需生成列。
- 从 restricted master 的 dual price 推导 pricing 子问题。
- 在切割库存上实现“解主问题—定价—加列”循环。
- 区分 LP 列生成、整数化与 branch-and-price。

## 前置回忆

切割库存：母卷长度 $L$，订单宽度 $w_i$、需求 $d_i$。一个 pattern $a$ 满足 $\sum_iw_i a_i\le L$。主问题最小化使用母卷数 $\sum_p x_p$，覆盖需求 $\sum_pa_{ip}x_p\ge d_i$。

## 完整精读讲解

所有可行 pattern 可能指数多。restricted master 先放少量列。其 dual 为最大化 $\sum_i d_i y_i$，每个已有 pattern 约束 $\sum_i a_{ip}y_i\le1$，$y_i\ge0$。dual price $y_i$ 表示多覆盖一件订单的边际价值。

新列的 reduced cost 是 $1-\sum_i a_i y_i$。定价因此是整数背包：在长度限制下最大化 $\sum_i y_i a_i$。若最优价格大于 1，找到负 reduced-cost 列并加入；若不超过 1，对所有隐含列的 dual 约束都满足，当前 restricted master 的 LP 解已是完整 master LP 最优。

这只是 LP 下界。把最后的列限制成整数再求，可能不是原整数问题最优，因为整数最优所需列在 LP 定价时从未有负 reduced cost。严谨精确法要 branch-and-price，在分支后继续定价，并设计与 pricing 兼容的 branching（如 Ryan–Foster）。

列生成易受 degeneracy 与 dual oscillation 影响：许多列 reduced cost 近零，dual 在极点间跳。可用 stabilization、一次加多列、列池和启发式定价。陷阱：约化费用符号反、初始 master 不可行、只检查已有列就错误停止、浮点阈值、把向上取整 LP 值当作已构造整数方案。

## 精确 60 分钟

- 00–07：写切割 pattern 与主问题。
- 07–20：推导 dual 和 reduced cost。
- 20–31：把 pricing 写成整数背包。
- 31–39：证明停止条件给完整 LP 最优。
- 39–53：运行小型列生成并读迭代日志。
- 53–58：用状态 DP 找整数切割方案。
- 58–60：区分列生成与 branch-and-price。

## 代码任务

从单一规格 patterns 开始；精确枚举小 dual 顶点；每轮定价并加列；停止后用覆盖状态 DP 构造整数方案，报告 LP 下界与整数上界。

## 验收标准

- 每个 pattern 不超过母卷长度。
- 终止时所有 pattern 的 price≤1（小实例全枚举复核）。
- 整数计划满足每类需求。
- 输出 LB≤整数最优/方案 UB，不混淆两者。

## 原始/权威资料

- Dantzig & Wolfe 1960：https://doi.org/10.1287/opre.8.1.101
- Gilmore & Gomory 1961 cutting stock：https://doi.org/10.1287/opre.9.6.849
- Desrosiers & Lübbecke 2005 Column Generation primer：https://doi.org/10.1007/0-387-25486-2_1
- SCIP/GCG 官方项目：https://gcg.or.rwth-aachen.de/
