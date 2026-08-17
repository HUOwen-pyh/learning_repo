# 第 21 晚：Benders 分解、对偶割与两阶段结构

## 学习目标

- 把 complicating variables 留在主问题，把连续 recourse 放入子问题。
- 从子问题对偶可行解生成全局有效 optimality cut。
- 子问题不可行时生成 feasibility cut。
- 正确维护 master 下界、incumbent 上界与停止条件。

## 前置回忆

第 11 晚：最小化 LP 子问题的对偶可行解给下界，最优对偶值等于子问题值。第 13 晚设施开设 $y$ 固定后，分配/供货常变成易解 LP。

## 完整精读讲解

两阶段模型可写 $\min\{f^\top y+Q(y):y\in Y\}$，其中
$Q(y)=\min\{q^\top x:Wx\ge h-Ty,x\ge0\}$。
主问题用变量 $\theta$ 近似 $Q(y)$。对子问题 dual 可行极点 $\pi$，弱对偶给
$Q(y)\ge\pi^\top(h-Ty)$，
所以加入 $\theta\ge\pi^\top(h-Ty)$。在当前 $\bar y$ 取最优 dual，割在 $\bar y$ 处紧，但对所有 y 都有效。

若子问题不可行，Farkas extreme ray 给 feasibility cut。简单供货模型中它退化为“开放总容量至少需求”。每轮解 restricted master 得全局 LB；把当前 y 放进真实子问题，若可行便得 $f^\top y+Q(y)$ 的 UB。若 UB−LB 在容差内停止。

multi-cut 按情景分别加割，通常更强但 master 更大；single-cut 聚合。Pareto-optimal cut、Magnanti–Wong、cut selection 与 warm start 可减少尾部迭代。Integer recourse 不满足普通 LP 强对偶，需要 logic-based Benders、combinatorial cuts 或更复杂 value-function 近似。

陷阱：用子问题 primal 解直接拼一个不保证全局有效的割、把只对当前 y 有效的逻辑条件漏掉、theta 无下界导致 master 无界、子问题不可行却强取 dual、LB/UB 方向反、在 time limit 把 incumbent 当最优。

## 精确 60 分钟

- 00–07：识别 master y、recourse x。
- 07–20：由子问题 dual 推导 optimality cut。
- 20–30：用 Farkas/容量推 feasibility cut。
- 30–39：画 LB/UB 迭代流程。
- 39–53：运行供货 Benders 并检查每条割。
- 53–58：与全开设枚举真值比较。
- 58–60：说明 integer recourse 的困难。

## 代码任务

主问题枚举二元开设变量但只看当前 cuts；子问题用连续贪心供货并构造 dual；记录 feasibility/optimality cuts、LB、UB，直到收敛。

## 验收标准

- 每条 dual cut 对所有 0-1 y 小实例枚举验证有效。
- LB 单调不降（重解精确 master 时），UB 不升。
- 最终 LB=UB=全枚举真值。
- 能解释为什么分解不是“分别局部最优再拼接”。

## 原始/权威资料

- Benders 1962 原论文：https://doi.org/10.1007/BF01386316
- Geoffrion 1972 Generalized Benders：https://doi.org/10.1007/BF00934810
- Rahmaniani et al. 2017 Benders survey：https://doi.org/10.1016/j.ejor.2016.12.005
- SCIP Benders 官方文档：https://www.scipopt.org/doc/html/BENDERS.php

