# 第 16 晚：旅行商、Held–Karp 子集 DP 与下界

## 学习目标

- 写出对称 TSP 的回路定义、degree constraints 与 subtour 问题。
- 从“已访问集合 + 末点”推导 Held–Karp DP。
- 重建最优回路，并用 1-tree/MST 型界理解上下界夹逼。
- 区分同名的 Held–Karp DP 与 Held–Karp LP/1-tree 下界。

## 前置回忆

哈密顿回路每个城市恰访问一次后回到起点。固定起点可消除旋转对称；对称距离下还可固定一个方向减少反转对称。子集可用 bitmask 表示。

## 完整精读讲解

度约束 $\sum_{e\in\delta(v)}x_e=2$ 只保证选出若干不相交环，不保证单一巡回；必须加入每个真子集 $S$ 的 subtour elimination $\sum_{e\in\delta(S)}x_e\ge2$。约束指数多，但可按需分离，这是 branch-and-cut 的典型来源。

Held–Karp DP 固定城市 0。状态 $DP[S,j]$ 是从 0 出发，恰访问 $S$（包含 0 与 j）并停在 j 的最短路径。转移
$DP[S,j]=\min_{i\in S\setminus\{j\}}DP[S\setminus\{j\},i]+d_{ij}$，
最后加 $d_{j0}$ 闭环。状态 $O(n2^n)$，转移总 $O(n^2 2^n)$，空间 $O(n2^n)$；比 $n!$ 好但仍指数。

下界方面，删掉起点后求其余点 MST，再加起点相连两条最便宜边，是任意巡回的下界（由巡回删去起点得到一棵/路径可连接结构；更标准的是最小 1-tree）。拉格朗日节点度约束可强化 1-tree，通常也称 Held–Karp bound。下界不必可行，上界必须来自真实巡回。

陷阱：非对称 TSP 仍用无向论证、距离不满足三角不等式却套度量近似、忘记闭环边、重建时 bit 位删除错误、把指数 DP 称“多项式”、下界计算错误超过已知可行回路。

## 精确 60 分钟

- 00–06：写 degree 模型并画两个 subtour 反例。
- 06–20：推导 DP 状态、转移、边界。
- 20–30：手算 4 城市两个 mask。
- 30–39：理解 MST/1-tree 下界与界方向。
- 39–53：运行 DP，重建并核验回路。
- 53–58：与全排列和下界比较。
- 58–60：写下时间/空间瓶颈。

## 代码任务

运行 Held–Karp DP，输出回路；对 8 城市以内用全排列核对；计算 MST 型下界，断言 lower bound≤OPT=DP=brute。

## 验收标准

- 回路恰含每城一次并回到起点。
- 距离逐边重算等于 DP 值。
- 可解释每个 bitmask 状态的语义。
- 不混淆 DP 与 LP/1-tree 下界。

## 原始/权威资料

- Held & Karp 1962 DP：https://doi.org/10.1137/0110015
- Held & Karp 1970 1-tree/拉格朗日：https://doi.org/10.1287/opre.18.6.1138
- Concorde TSP 官方项目：https://www.math.uwaterloo.ca/tsp/concorde.html

