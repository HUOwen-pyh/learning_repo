# 第 23 晚：Concurrent Flow、Sparsest Cut 与 flow-cut gap

## 目标

建模最大并发流与最小拥塞；理解 cut 是对偶证书但未必精确；用小路径集枚举分流比例，观察多商品 flow-cut gap。

## 前置回忆（5 分钟）

有需求对 `(s_i,t_i,d_i)`。若全部需求按共同倍率 λ 发送，任意 cut S 对 λ 给出什么上界？分子是 cut capacity，分母是什么？

## 精读正文（20 分钟）

Maximum Concurrent Flow 最大化 λ，使每个商品 i 发送 `λd_i` 且共享边容量。对任意 cut，跨 cut 的需求总量 `D(S)` 必须穿过容量 `C(S)`，故 `λ<=C(S)/D(S)`；最小这个比值就是 sparsest-cut 上界。

单商品有 max-flow=min-cut；多商品一般不相等。无向图中的 flow-cut gap 最坏为 `Θ(log n)`（依模型常数/需求定义），它既解释用 cut LP 舍入的 `O(log n)` 近似，也与 metric embedding 紧密相连。Leighton–Rao 用多商品流给 uniform sparsest cut 的 `O(log n)` 近似；后续 SDP/负型度量改进某些版本。不要把“gap O(log n)”误说成所有特例都差这么多，树上路径唯一时可精确计算拥塞。

代码采用两商品、每商品两条候选路径，每条流按比例 q 分到路径 0/1；枚举细网格求最小最大边拥塞 `ρ`，并枚举顶点 cut 得下界 `ρ>=max_S D(S)/C(S)`（等价 λ 方向取倒数）。这是 path-restricted 教学模型；若候选路径未包含所有简单路径，所得 ρ 可能高于真正 LP OPT。

前沿连接：乘权算法把每商品的最短路当 oracle；cut-matching games、低拥塞嵌入和近线性时间流算法仍是活跃工具。读论文先核对 directed/undirected、edge/node capacity 与 product/sum demand 定义。

## 精确 60 分钟

- 00–05：推导 cut 上界。
- 05–25：写 concurrent-flow LP 的守恒与容量约束。
- 25–45：运行两商品网格分流与 cut 枚举。
- 45–55：删一条候选路径，观察“受限模型”值变差。
- 55–60：解释单商品等式为何不推广。

## 代码实验

脚本在固定四点图及随机容量上枚举两个 split 参数，返回最小拥塞；所有 cut 给出的拥塞下界都用断言核验。

## 验收

- 能在 λ 与 ρ=1/λ 两种方向正确写 cut 界。
- 能解释 path restriction 的影响。
- 能陈述 flow-cut gap 的模型依赖。

## 原始/权威资料

- Leighton & Rao (1999), Multicommodity max-flow min-cut theorems and their use: <https://doi.org/10.1145/331524.331526>
- Linial, London & Rabinovich (1995), The geometry of graphs and some of its algorithmic applications: <https://doi.org/10.1007/BF02574050>

