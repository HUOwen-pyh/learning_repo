# 第 08 晚：MST、Euler 化与 metric TSP 2-近似

## 目标

证明 preorder/double-tree 算法是 metric TSP 2-近似；明确三角不等式与完备度量闭包的作用；实现 MST 与 shortcut。

## 前置回忆（5 分钟）

从任意 Hamilton 回路删一条边得到什么？为什么 MST 成本不超过 OPT？写出三角不等式 `d(a,c)<=d(a,b)+d(b,c)`。

## 精读正文（20 分钟）

算法先求 MST `T`，把每条树边走两次得到成本 `2c(T)` 的 Euler 闭游；按首次到达顺序 shortcut 重复顶点，最后回起点。度量三角不等式保证用直达边替换一段路径不会增重，因此 `ALG<=2c(T)<=2OPT`。代码等价地做树的 DFS preorder，然后按该顺序成环。

完整复杂度在稠密距离矩阵上 Prim 为 `O(n^2)`，DFS `O(n)`。若输入是不完备连通图，先取全点对最短路形成 metric closure；shortcut 的边对应原图路径。若存在负边或距离不满足三角不等式，shortcut 可能变贵，保证完全失效。甚至一般（非度量）TSP 不存在任何常数比近似，除非 `P=NP`，可用“存在边权 1、不存在边权巨大的 Hamilton 回路 gap”理解。

MST 下界可能很松：树的回溯付两遍，而最优 tour 可巧妙连接奇度顶点。下一晚 Christofides 只复制一组最小匹配，把 `2` 降到 `3/2`。反例意识：仅输出 preorder 路径而忘记回起点不是 TSP tour；距离矩阵非对称时 DFS shortcut 分析也不直接成立。

## 精确 60 分钟

- 00–05：写 MST 下界。
- 05–25：画树、Euler 游和 shortcut，标三处不等式。
- 25–45：运行代码，与排列穷举 OPT 对拍。
- 45–55：生成破坏三角不等式的反例。
- 55–60：口述完备图与 metric closure 的关系。

## 代码实验

脚本用欧氏点产生度量矩阵，Prim 建树、preorder 成 tour，并对 `n<=9` 穷举固定起点的 tour，断言 `ALG<=2OPT` 及 `ALG<=2MST`。

## 验收

- 能解释删 tour 一边给 MST 下界。
- 能指出 shortcut 唯一依赖的性质。
- 能写出算法完整复杂度。

## 原始/权威资料

- Rosenkrantz, Stearns & Lewis (1977), An analysis of several heuristics for TSP: <https://doi.org/10.1137/0206041>
- Williamson & Shmoys，第 2.4 节：<https://www.designofapproxalgs.com/book.pdf>

