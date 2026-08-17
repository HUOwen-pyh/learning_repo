# 第 09 晚：Christofides 的奇点匹配与 3/2

## 目标

实现 Christofides；证明奇度点最小完美匹配成本不超过 `OPT/2`；理解 Euler shortcut、匹配 oracle 与现代 TSP 边界。

## 前置回忆（5 分钟）

握手定理为何保证奇度顶点数为偶数？一个连通多重图何时有 Euler 回路？回忆 MST `<=OPT`。

## 精读正文（20 分钟）

求 MST `T`，令 `O` 为其奇度顶点集；在 `O` 的度量完全图上求最小权完美匹配 `M`。`T∪M` 连通且所有度数为偶数，求 Euler 回路并 shortcut，得到 Hamilton tour。

关键界：取最优 TSP tour，只看 `O` 中顶点，按 tour 顺序 shortcut 得到 `O` 上一个环，成本不超过 OPT。这个偶数环交替拆成两个完美匹配，所以较便宜者至多 OPT/2；最小匹配 `c(M)` 不更贵。故 `ALG<=c(T)+c(M)<=OPT+OPT/2`。注意不能随便在原 tour 的边上“取交替边”，因为 `O` 顶点之间可能隔着其他点，必须先用度量 shortcut。

代码对小奇点集用 `O((|O|-1)!!)` 递归 DP 求匹配；工业实现应用 Blossom。Euler 多重边必须用 edge id，不能用集合去重。Christofides 的经典界 3/2；2021 年 Karlin–Klein–Oveis Gharan 给出首个一般 metric TSP 的 `3/2-ε` 随机近似（ε 极小），不是对 Christofides 原算法的简单重分析。非对称 metric TSP 是另一难题，已知常数算法的常数远大。

## 精确 60 分钟

- 00–05：证明奇点偶数。
- 05–25：独立写出匹配 `<=OPT/2` 的每一步。
- 25–45：运行 MST+matching+Euler+shortcut。
- 45–55：故意去重平行边，观察 Euler 断言失败。
- 55–60：准确说出经典界与现代突破差别。

## 代码实验

脚本对欧氏小实例与排列 OPT 对拍，并显式检查多重图每点偶度、Euler 使用每条边一次、结果为排列。

## 验收

- 能解释为何存在两个交替匹配。
- 能说明平行边不能丢。
- 不把 `3/2-ε` 说成确定性大幅改进。

## 原始/权威资料

- Christofides (1976), Worst-case analysis of a new heuristic for TSP: <https://www.cs.cmu.edu/~15854/handouts/christofides.pdf>
- Karlin, Klein & Oveis Gharan (STOC 2021), A (slightly) improved approximation algorithm for metric TSP: <https://doi.org/10.1145/3406325.3451009>

