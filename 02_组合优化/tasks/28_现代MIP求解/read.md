# 第 28 晚：现代 MIP 求解器的 branch-cut-price 机器

## 学习目标

- 把 presolve、LP relaxation、cuts、heuristics、branching、conflict 串成求解循环。
- 读懂 primal bound、dual bound、gap、nodes、LP iterations 与状态。
- 理解数值缩放、容差、determinism 和 proof/certificate 的重要性。
- 建立现代 MIP、可验证求解与学习增强的研究入口。

## 前置回忆

回忆第 17 晚搜索树、第 18 晚 cuts、第 20 晚 columns。生产求解器不是单一算法，而是这些组件和大量控制策略的组合。

## 完整精读讲解

求解通常从 presolve 开始：固定变量、删冗余行、收紧界、聚合、检测蕴含整数性与对称。根节点解 LP，分离 clique/cover/MIR/Gomory/flow-cover 等割；primal heuristics（rounding、diving、RINS、local branching）尽早找 incumbent；branching 选择变量/约束，节点中继续传播、reoptimization 和 cut。

最小化日志中 primal bound 来自整数可行解，是上界；dual bound 来自所有开放节点松弛，是下界。状态 OPTIMAL 需 gap/容差满足且证书链完成；FEASIBLE/TIME_LIMIT 只给 incumbent。MIP start、solution pool、time/node/gap limits 都改变停止语义。公平 benchmark 要固定版本、线程、seed、时间、硬件并用 shifted geometric mean，避免只挑胜例。

数值上，过大 Big-M、系数量级跨度、近相等约束会导致 ill-conditioning。integrality tolerance 意味着 0.999999 可能被视为整数，但不能让 Big-M 放大成巨大业务违约。重算 residual、缩放模型，必要时用有理/精确模式和可独立验证 proof。

现代研究包括：学习 branching/cut/heuristic 策略、神经 warm start、算法配置与 foundation model；关键风险是分布外泛化、推理开销、可复现性和保持求解正确性。学习通常只选择策略，不应破坏 bound/certificate。SCIP 10 的精确有理 MILP 与 VIPR 证书是 2025–2026 的重要可验证求解入口。

## 精确 60 分钟

- 00–08：画 branch-and-cut 数据流。
- 08–20：逐项解释一段虚拟 solver log。
- 20–31：连接 presolve/heuristic/dual bound。
- 31–40：分析 Big-M 与整数容差漏洞。
- 40–53：运行 mini set-cover solver 看组件统计。
- 53–58：对照 MIPLIB/SCIP/HiGHS 入口。
- 58–60：写明每个停止状态能证明什么。

## 代码任务

实现小型 set-cover 精确求解器：支配 presolve、greedy incumbent、可行 dual lower bound、best-bound 搜索和独立检查；与全枚举真值核对并输出节点统计。

## 验收标准

- presolve 不删任何可能改善的列（用小实例真值核验）。
- dual bound 从显式对偶可行权重得到。
- incumbent 始终可行，最终等于穷举 OPT。
- 能根据 log 区分 primal/dual bound 与 time limit。

## 原始/权威资料与前沿入口（已核验）

- SCIP 10.0 官方技术报告（2025）：https://optimization-online.org/2025/11/the-scip-optimization-suite-10-0/
- SCIP 最新 branch-cut-price 文档：https://scipopt.org/doc/html/
- HiGHS 官方文档（LP/MIP/QP）：https://highs.dev/
- MIPLIB 2017 官方 benchmark：https://miplib.zib.de/
- Gasse et al. 2019 Learning to Branch：https://papers.nips.cc/paper/2019/hash/d14c2267d848abeb81fd590f371d39bd-Abstract.html
- VIPR 可验证整数规划结果：https://optimization-online.org/2016/11/5740/

