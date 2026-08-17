# 第 12 晚：Unrelated Machines 的分槽 LP 舍入

## 目标

读懂 `R||Cmax` assignment LP；实现 Shmoys–Tardos 分槽与二分图匹配；证明给定阈值 `T` 的可行 LP 可舍入到 makespan `<2T`。

## 前置回忆（5 分钟）

无关机上作业 `j` 在机器 `i` 的时长是 `p_ij`。写变量 `x_ij`，约束 `Σ_i x_ij=1`、`Σ_j p_ijx_ij<=T`。为何可先禁止 `p_ij>T` 的边？

## 精读正文（20 分钟）

对每台机器，把 `x_ij>0` 的作业按 `p_ij` 非增排序，并将分数质量依次装进容量 1 的 slot；每个分片连一条“作业—slot”边。原 `x` 给出了覆盖所有作业的分数匹配，因此 Hall 条件成立，二分图有匹配把每项完整指派到一个 slot。

负载界是分槽技巧的精髓。除第一个 slot 的首个（最大）作业外，其余被匹配作业的处理时间可按 slot 边界向前收费给分数负载；总计至多 `Σ_j p_ijx_ij + max_{j:x_ij>0}p_ij <= T+T=2T`。更严谨写法比较第 `k` 个 slot 被指派作业与前一 slot 的分数片段。LP 可行性给第一个 T，删除长边给第二个 T。

完整 LST 算法二分搜索 T 并求 LP，可得 2-近似；本练习不用第三方求解器，输入一个可行分数解并验证“舍入内核”。代码生成凸组合分配作为测试前提，不能声称它求得 LP 最优。反例：若不按时长降序装槽，收费关系消失；若保留 `p_ij>T` 正质量，只能保证 `T+pmax`，未必 2T。

## 精确 60 分钟

- 00–05：写 assignment LP。
- 05–25：画一台机器的三个 slot 与跨边界分片。
- 25–45：运行打包、增广路匹配和负载断言。
- 45–55：打乱排序，搜索违反 2T 的例子。
- 55–60：说明代码实现的是 rounding oracle 而非 LP solver。

## 代码实验

脚本构造每个作业分配和为 1 的分数矩阵，令 T 覆盖分数负载与支持边最大时长，舍入后检查每作业恰一次、每机负载 `<=2T`。

## 验收

- 能写出 LP 三类约束。
- 能解释排序为何让“向前收费”成立。
- 能区分 LP 求解与 LP 舍入。

## 原始/权威资料

- Lenstra, Shmoys & Tardos (1990), Approximation algorithms for scheduling unrelated parallel machines: <https://doi.org/10.1007/BF01585745>
- Shmoys & Tardos (1993), An approximation algorithm for the generalized assignment problem: <https://doi.org/10.1007/BF01187672>

