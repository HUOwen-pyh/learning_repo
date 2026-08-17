# 组合优化：30 个夜晚，从模型到现代求解器

这是一条每天严格 60 分钟的自学路线。目标不是背算法名，而是形成四种可以迁移的能力：

1. 把业务语言翻译为变量、目标、约束与可验证的假设；
2. 识别图、流、匹配、拟阵、LP/IP、动态规划和分解结构；
3. 同时给出可行解（上界）与松弛/对偶证书（下界），用 gap 判断还差多远；
4. 读懂现代 MIP/CP-SAT 求解日志，并能设计小型精确算法、启发式与实验。

## 使用方法

- 每晚先打开对应 read.md，严格按其中的分钟表推进；不要把阅读挤占代码时间。
- practice.py 只用 Python 3.11+ 标准库，初始状态可直接运行。先运行并读懂断言，再完成文件末尾的“动手改造”。
- 每次实验记录：实例规模、目标值、可行性、下界/上界、gap、运行时间、随机种子。只报一个目标值不算完成。
- 若一晚卡住，先保留失败用例和猜想，次日开始前最多补 10 分钟；不要无限延期。

运行单晚：

    python tasks/06_最大流最小割/practice.py

在本目录用 PowerShell 运行全部练习：

    Get-ChildItem tasks -Recurse -Filter practice.py |
      Sort-Object FullName |
      ForEach-Object { python $_.FullName; if ($LASTEXITCODE) { throw $_ } }

## 30 晚路线图

| 晚 | 主题 | 核心产出 |
|---:|---|---|
| 01 | [建模与证书](tasks/01_建模与证书/read.md) | 从自然语言得到 0-1 模型、可行性检查器和上下界 |
| 02 | [图结构与状态空间](tasks/02_图结构与状态空间/read.md) | 表示图、拓扑序、SCC 与状态图 |
| 03 | [最短路](tasks/03_最短路/read.md) | Dijkstra、Bellman-Ford、负环证书 |
| 04 | [最小生成树](tasks/04_最小生成树/read.md) | cut/cycle 性质、Kruskal 与 Prim |
| 05 | [二分图匹配](tasks/05_二分图匹配/read.md) | 增广路、Kőnig 定理、Hopcroft–Karp |
| 06 | [最大流最小割](tasks/06_最大流最小割/read.md) | 残量网络、Dinic、割证书 |
| 07 | [最小费用流](tasks/07_最小费用流/read.md) | 势函数、约化费用、逐次最短路 |
| 08 | [指派与匈牙利算法](tasks/08_指派与匈牙利算法/read.md) | 指派 LP、对偶标号、O(n³) 算法 |
| 09 | [拟阵与贪心](tasks/09_拟阵与贪心/read.md) | 交换公理、秩函数、贪心刻画 |
| 10 | [线性规划几何](tasks/10_线性规划几何/read.md) | 顶点、基、单纯形直觉与数值风险 |
| 11 | [对偶与互补松弛](tasks/11_对偶与互补松弛/read.md) | 弱/强对偶、Farkas、最优性证书 |
| 12 | [全单模与整数性](tasks/12_全单模与整数性/read.md) | TU、网络矩阵、何时 LP 自动给整数解 |
| 13 | [整数规划建模](tasks/13_整数规划建模/read.md) | Big-M、扩展公式、对称性与强公式 |
| 14 | [松弛与整数间隙](tasks/14_松弛与整数间隙/read.md) | LP 下界、舍入、gap 与反例 |
| 15 | [背包动态规划](tasks/15_背包动态规划/read.md) | 伪多项式 DP、支配、FPTAS 入口 |
| 16 | [旅行商与子集DP](tasks/16_旅行商与子集DP/read.md) | Held–Karp、1-tree/子回路松弛视角 |
| 17 | [分支定界](tasks/17_分支定界/read.md) | 界、分支、节点策略和最优性 gap |
| 18 | [割平面](tasks/18_割平面/read.md) | CG/Gomory/cover cut 与分离 |
| 19 | [拉格朗日松弛](tasks/19_拉格朗日松弛/read.md) | 松弛难约束、次梯度、原始恢复 |
| 20 | [列生成](tasks/20_列生成/read.md) | Dantzig–Wolfe、定价、切割库存 |
| 21 | [Benders分解](tasks/21_Benders分解/read.md) | 主问题、子问题、可行性/最优性割 |
| 22 | [次模优化](tasks/22_次模优化/read.md) | 边际递减、最大覆盖与 1−1/e |
| 23 | [多面体组合](tasks/23_多面体组合/read.md) | facet、分离-优化等价与 TSP 割 |
| 24 | [局部搜索与元启发式](tasks/24_局部搜索与元启发式/read.md) | 邻域、2-opt、退火和可复现实验 |
| 25 | [在线优化](tasks/25_在线优化/read.md) | 竞争比、对手模型与 Ranking |
| 26 | [随机优化](tasks/26_随机优化/read.md) | 两阶段模型、SAA、样本外评估 |
| 27 | [鲁棒优化](tasks/27_鲁棒优化/read.md) | 不确定集、预算鲁棒与保守度 |
| 28 | [现代MIP求解](tasks/28_现代MIP求解/read.md) | presolve、cut、heuristic、branch-and-cut |
| 29 | [CP-SAT与调度](tasks/29_CP-SAT与调度/read.md) | 传播、冲突学习、全局约束、作业车间 |
| 30 | [综合项目](tasks/30_综合项目/read.md) | 设施选址的精确法、启发式与情景压力测试 |

## 阶段验收

- 第 1–9 晚：能从零实现图优化原语，并输出独立可核验的路径、树、匹配或割。
- 第 10–16 晚：能解释 primal/dual、整数性来源、松弛强弱和 DP 的状态设计。
- 第 17–23 晚：能把“求一个大问题”拆成搜索树、割、定价或子问题，并维护界。
- 第 24–29 晚：能区分启发式结果与最优性证明，正确设计在线/随机/鲁棒实验，读懂现代求解器组件。
- 第 30 晚：在一个统一模型中交付数据、算法、证书、实验与局限说明。

## 推荐主教材与基准

- Korte & Vygen, Combinatorial Optimization（Springer）：https://doi.org/10.1007/978-3-662-56039-6
- Schrijver, Combinatorial Optimization（Springer）：https://doi.org/10.1007/978-3-540-44489-8
- Nemhauser & Wolsey, Integer and Combinatorial Optimization：https://doi.org/10.1002/9781118627372
- Williamson & Shmoys, The Design of Approximation Algorithms（作者开放版）：https://www.designofapproxalgs.com/
- MIPLIB 2017 基准库（官方）：https://miplib.zib.de/
- DIMACS Implementation Challenges：https://dimacs.rutgers.edu/programs/challenge/

本课程的代码刻意不依赖外部求解器，以暴露算法骨架；第 28–29 晚会把这些骨架映射到 HiGHS、SCIP 与 OR-Tools CP-SAT 的实际接口和日志。
