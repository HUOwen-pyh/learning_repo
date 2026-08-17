# 第 15 晚：背包动态规划、支配与 FPTAS

## 学习目标

- 从“前 i 件、容量 b”推导 0-1 背包状态转移。
- 区分按重量 DP 的伪多项式复杂度与真正多项式。
- 用价值缩放理解背包 FPTAS 的误差—时间折中。
- 重建物品集合并独立核验，而不只返回最优值。

## 前置回忆

每件物品只能取 0 或 1 次。状态 $DP[i,b]$ 表示前 $i$ 件在容量 $b$ 下最大价值；选择第 $i$ 件时从上一行的 $b-w_i$ 转移，不能在同一行正序更新造成重复取用。

## 完整精读讲解

转移为 $DP[i,b]=\max(DP[i-1,b],DP[i-1,b-w_i]+v_i)$。时间 $O(nB)$、空间可压到 $O(B)$；但输入中的 $B$ 只需 $\log B$ 位，所以这不是关于输入长度的多项式算法，称伪多项式。这也解释弱 NP-hard 与数值大小的关系。

另一视角以总价值为状态，记录达到价值至少/恰为 $p$ 的最小重量。把价值缩放：令 $K=\varepsilon V_{\max}/n$，$\hat v_i=\lfloor v_i/K\rfloor$，在缩放价值上做最小重量 DP。每件舍入损失小于 $K$，总损失小于 $nK=\varepsilon V_{\max}\le\varepsilon OPT$，故返回至少 $(1-\varepsilon)OPT$。状态总价值 $O(n^2/\varepsilon)$，典型复杂度 $O(n^3/\varepsilon)$，是 FPTAS。

支配可删状态：若状态 A 重量不大于 B 且价值不小于 B，B 永远不优。稀疏 Pareto frontier 对大容量常有优势，但最坏仍指数。工程陷阱包括零重量正价值、负价值、重建指针被一维覆盖、浮点 K 为零、用整数截断方向错误，以及把 unbounded knapsack 的正序更新套到 0-1。

## 精确 60 分钟

- 00–07：手填 4 件物品 DP 表。
- 07–18：推导转移并解释更新方向。
- 18–28：从输入位长解释伪多项式。
- 28–39：推导 FPTAS 的舍入损失界。
- 39–53：运行精确 DP 与缩放 DP。
- 53–58：改变 epsilon 记录质量/状态数。
- 58–60：口述 $(1-\varepsilon)$ 保证链。

## 代码任务

实现精确重量 DP 与价值缩放 FPTAS；两者返回物品索引；检查容量、重算价值，并断言近似值达到理论保证。

## 验收标准

- 0-1 物品不会被重复选。
- 返回集合的重量/价值与表值一致。
- 至少测试两个 epsilon，较小 epsilon 不减少缩放精度。
- 能解释 $O(nB)$ 为什么不是输入长度多项式。

## 原始/权威资料

- Ibarra & Kim 1975 背包 FPTAS：https://doi.org/10.1145/321906.321909
- Kellerer, Pferschy & Pisinger, Knapsack Problems：https://doi.org/10.1007/978-3-540-24777-7
- Martello & Toth, Knapsack Problems：https://onlinelibrary.wiley.com/doi/book/10.1002/9781118033349
