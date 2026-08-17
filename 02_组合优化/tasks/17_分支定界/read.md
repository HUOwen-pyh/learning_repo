# 第 17 晚：分支定界、搜索树与 gap

## 学习目标

- 用 relaxation bound、incumbent 与 branching 构造完整性证明。
- 区分 best-bound、depth-first 和 hybrid 节点策略。
- 在 0-1 背包上实现分数上界的 branch-and-bound。
- 正确报告绝对/相对 gap 与终止原因。

## 前置回忆

最大化问题中，可行 incumbent 是全局下界；每个未解节点的松弛值是该子树上界。若节点上界不超过 incumbent，可安全剪枝。

## 完整精读讲解

分支定界维护对子问题的划分。分支必须覆盖父节点所有整数解且子节点并集完整，例如 $x_j=0$ 与 $x_j=1$。定界用容易问题包住难问题；背包按密度装满并允许最后一件分数取用，得到该节点可靠上界。若节点不可行、松弛已整数、或 bound 不优于 incumbent 就 fathom。

best-bound 优先处理全局上界最大的节点，通常较快证明 gap；DFS 内存小且较快找深层可行解；实际用 diving、restart、混合策略。分支变量影响树大小：strong branching 试解候选子节点获得高质量决策，代价高；pseudo-cost 从历史估计。

全局最大上界是所有开放节点 bound 的最大值。最大化相对 gap 可写 $(UB-LB)/\max(|LB|,\epsilon)$，但不同求解器分母约定不同，必须声明。达到时间限制只说明当前 incumbent 与 bound，不代表最优；只有开放节点耗尽或 gap 达阈值才有相应证书。

复杂度最坏仍指数；好的界和 incumbent 改变实例表现但不改变 NP-hard 性。浮点 bound 向错误方向舍入会误剪最优解，生产求解器使用容差/安全舍入。其他陷阱：分数上界排序与原索引重建混乱、容量超限节点仍计算 bound、相等时错误丢失所有最优解（若只需一个最优则可剪）。

## 精确 60 分钟

- 00–07：画三层搜索树并标 LB/UB。
- 07–19：推导分数背包节点上界。
- 19–30：比较三种节点策略。
- 30–39：理解剪枝完整性与 gap。
- 39–53：运行 best-bound 实现并看统计。
- 53–58：关闭贪心 incumbent，比较节点数。
- 58–60：说明时间限制输出能证明什么。

## 代码任务

实现优先队列 branch-and-bound；输出展开、界剪、不可行剪数量；与穷举/DP 最优值核对，并验证返回集合。

## 验收标准

- 每个剪枝都有明确且方向正确的证据。
- 返回物品不重复、容量可行、价值重算一致。
- 全局 bound 不低于 incumbent（未结束时）。
- 能解释最坏指数与实践加速不矛盾。

## 原始/权威资料

- Land & Doig 1960 分支定界原论文：https://doi.org/10.1080/14786436008238308
- Linderoth & Savelsbergh 1999 搜索策略综述：https://doi.org/10.1287/ijoc.11.2.173
- SCIP branching 官方文档：https://www.scipopt.org/doc/html/BRANCH.php

