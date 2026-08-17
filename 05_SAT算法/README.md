# SAT 算法：30 晚从 DPLL 到现代可验证求解

这条路线用 30 个一小时单元构造一个 SAT 求解器的完整心智模型。每晚先读 `read.md`，再运行同目录 `practice.py`。代码只依赖 Python 3.11+ 标准库，规模故意保持可穷举验证；目标是掌握正确性与实验方法，而非在 Python 中追赶 C++ 竞赛求解器。

## 固定节奏

0–5 分钟闭卷回忆；5–25 分钟精读；25–50 分钟运行并完成“动手改造”；50–57 分钟加入正例/反例/边界测试；57–60 分钟写下不变量、一个失败模式和下一步。脚本断言通过只是开始，能解释为何正确才算完成。

## 阶段路线

| 阶段 | 晚次 | 产出 |
|---|---:|---|
| 语义与基础搜索 | 01–06 | DIMACS、Tseitin、DPLL、传播、预处理、分支 |
| CDCL 正确性骨架 | 07–10 | trail、决策层、1-UIP、学习和回跳 |
| CDCL 性能工程 | 11–16 | VSIDS、重启、LBD、watch、inprocessing、BVE |
| 接口与可信结果 | 17–18 | incremental assumptions、UNSAT core、proof logging |
| 特殊推理与扩展 | 19–27 | 随机相变、WalkSAT、XOR、cardinality、MaxSAT、SMT、BMC、#SAT、并行 |
| 现代研究与综合 | 28–30 | profiling、竞赛/外部传播前沿、MiniCDCL 报告 |

## 任务索引

01. [布尔逻辑、CNF 与 DIMACS](tasks/01_布尔逻辑_CNF与DIMACS/read.md)
02. [Tseitin 转换与等可满足编码](tasks/02_Tseitin等可满足编码/read.md)
03. [穷举、回溯与 DPLL 骨架](tasks/03_穷举与DPLL骨架/read.md)
04. [单位传播与双监视文字](tasks/04_单位传播与双监视文字/read.md)
05. [纯文字、重言式与基础预处理](tasks/05_纯文字与基础预处理/read.md)
06. [分支启发式：MOMS、Jeroslow–Wang 与 DLIS](tasks/06_分支启发式_MOMS_JW/read.md)
07. [Trail、理由与决策层](tasks/07_Trail与决策层/read.md)
08. [蕴含图、冲突分析与 First-UIP](tasks/08_蕴含图与First_UIP/read.md)
09. [CDCL：学习与非时间回溯的最小闭环](tasks/09_CDCL最小闭环/read.md)
10. [学习子句、断言性与回跳验证](tasks/10_学习子句与回跳验证/read.md)
11. [VSIDS、EVSIDS 与活动度维护](tasks/11_VSIDS与EVSIDS/read.md)
12. [Phase Saving 与 Luby 重启](tasks/12_PhaseSaving与Luby重启/read.md)
13. [LBD、子句活动度与学习库删减](tasks/13_LBD与学习库删减/read.md)
14. [工程级双监视传播与不变量测试](tasks/14_工程级双监视传播/read.md)
15. [Subsumption、SSR 与阻塞子句消去](tasks/15_Subsumption_SSR与BCE/read.md)
16. [有界变量消去、Resolution 与模型重建](tasks/16_有界变量消去与模型重建/read.md)
17. [增量 SAT、假设与 UNSAT Core](tasks/17_增量SAT_假设与UNSATCore/read.md)
18. [Resolution、DRAT/LRAT 与可检查 UNSAT 证明](tasks/18_DRAT_LRAT与可检查证明/read.md)
19. [随机 k-SAT、相变与实验方法](tasks/19_随机kSAT与相变/read.md)
20. [GSAT、WalkSAT 与随机局部搜索](tasks/20_GSAT与WalkSAT局部搜索/read.md)
21. [XOR 约束、GF(2) 高斯消元与 CDCL(XOR)](tasks/21_XOR约束与高斯消元/read.md)
22. [基数约束：pairwise、sequential 与 cardinality network](tasks/22_基数约束编码/read.md)
23. [Pseudo-Boolean、MaxSAT 与线性搜索](tasks/23_PseudoBoolean与MaxSAT/read.md)
24. [DPLL(T)：SAT 与理论求解器协作](tasks/24_DPLL_T与SMT骨架/read.md)
25. [有界模型检查：转移系统到 SAT](tasks/25_有界模型检查编码/read.md)
26. [AllSAT、#SAT、阻塞子句与组件缓存](tasks/26_AllSAT与SharpSAT/read.md)
27. [并行 Portfolio、Clause Sharing 与 Cube-and-Conquer](tasks/27_Portfolio与CubeAndConquer/read.md)
28. [内存布局、热路径与可复现基准](tasks/28_求解器工程与性能测量/read.md)
29. [现代 SAT 前沿：竞赛、外部传播与可验证求解](tasks/29_现代SAT前沿与竞赛复现/read.md)
30. [综合项目：MiniCDCL、证书与基准报告](tasks/30_综合项目_MiniCDCL/read.md)

## 版本与前沿边界

资料快照为 2026-08。现代基线以 [CaDiCaL](https://github.com/arminbiere/cadical)、[MiniSat](https://github.com/niklasso/minisat) 和 [SAT Competition 2025](https://satcompetition.github.io/2025/) 的公开源码/规则为入口。竞赛主赛道要求 UNSAT proof；课程因此把“输出答案”和“独立验证证据”分开。机器学习、GPU 和外部传播均是活跃方向，但第29晚只做受控 ablation，不把小型实验称为前沿性能突破。

## 结课验收

你应能从零解释并实现 CNF 语义、BCP、watcher、trail、1-UIP、回跳、VSIDS、重启、LBD 与安全删除；能分清 equisatisfiable、equivalent、SAT model、UNSAT proof、subset-minimal core；能对随机与结构化实例做可复现实验；能把 SAT oracle用于MaxSAT/SMT/BMC/#SAT，同时准确声明其保证边界。
