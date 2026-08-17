# 第 29 晚：CP-SAT、传播、冲突学习与作业车间

## 学习目标

- 用 interval、precedence、NoOverlap 表达 job-shop。
- 理解 domain propagation、SAT clause、conflict learning 与 lazy clause generation。
- 用 disjunctive graph 的方向变量实现小型精确调度。
- 知道何时优先 CP-SAT，何时 MIP/专用算法更合适。

## 前置回忆

每个操作有 start、duration、end；同一 job 的操作按顺序；同一 machine 上任意两个 interval 不得重叠。两操作 a,b 的不重叠是 $(a\prec b)\lor(b\prec a)$。

## 完整精读讲解

CP 以变量 domain 和 constraint propagator 为核心。若一个机器只有一个空档能容纳任务，传播可删其他开始时间；edge-finding、energetic reasoning 从一组 interval 的总处理量推更强界。搜索选择变量和值，失败后回溯。

SAT/CDCL 把布尔决策形成 clauses。冲突分析从 implication graph 学得 no-good，并 non-chronological backtrack。Lazy Clause Generation 让 CP propagator 说明每次推理的布尔原因，从而把全局约束结构与 SAT 学习结合。CP-SAT 还整合整数线性传播、LP relaxation、cuts、portfolio workers 和 LNS；模型必须用整数系数/变量，连续小数要谨慎缩放。

job-shop 的 disjunctive graph 固定 job precedence arcs，对同机器每对操作选择一个方向。若产生有向环，该部分赋值不可扩展，可立即剪；若无环，最长路给最早开始和 makespan 下界。枚举所有方向是指数级，但展示了 CP 的 branching、cycle propagation、critical-path bound。

CP-SAT 常适合富逻辑、排程、可选 interval、all-different；MIP 对强线性松弛、连续变量、可解释 dual bound 很成熟。实际应做并行基准而非教条选择。陷阱：把浮点直接传 CP-SAT、NoOverlap 漏 optional presence、时间 horizon 过大、只取 FEASIBLE 状态却称最优、回调中耗时过多。

## 精确 60 分钟

- 00–07：画 job-shop interval 甘特图。
- 07–19：写 precedence 与 disjunction。
- 19–30：追踪一次传播—冲突—学习。
- 30–39：用 DAG longest path 得 makespan LB。
- 39–53：运行方向搜索并验证 schedule。
- 53–58：阅读官方 job-shop/CP-SAT 状态。
- 58–60：写一个 CP-SAT vs MIP 选择理由。

## 代码任务

对 3×3 job-shop，递归决定机器 pair 顺序；每次增 arc 检测环并用 critical path 下界剪枝；输出最优 start/makespan，独立检查 job precedence 与机器不重叠。

## 验收标准

- 每操作开始非负、完成不晚于 makespan。
- 所有 job precedence 与 machine NoOverlap 通过。
- cycle/critical-bound 剪枝计数非零。
- 返回值与已知小实例最优 11 一致。

## 原始/权威资料与前沿入口（已核验）

- OR-Tools CP-SAT 官方指南：https://developers.google.com/optimization/cp/cp_solver
- OR-Tools job-shop 官方示例：https://developers.google.com/optimization/scheduling/job_shop
- Perron, Didier & Gay 2023, The CP-SAT-LP Solver：https://doi.org/10.4230/LIPIcs.CP.2023.3
- OR-Tools SAT 官方源代码文档：https://github.com/google/or-tools/tree/stable/ortools/sat
- Schutt et al. 2009 Lazy Clause Generation：https://doi.org/10.1007/978-3-642-04244-7_22

