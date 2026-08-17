# 第 22 晚：从 max-flow 到 fractional packing 的乘权更新

## 目标

把路径流写成 packing LP；理解 multiplicative weights 如何把拥塞边变贵；实现小型路径打包器，并用网格 oracle 检查可行性和质量。

## 前置回忆（5 分钟）

单商品 max-flow 的路径 LP：每条 s-t 路径变量 `x_P>=0`，每边 `e` 有 `Σ_{P∋e}x_P<=c_e`，目标是什么？对偶的边长度需让每条路径满足什么？

## 精读正文（20 分钟）

路径 packing LP 最大化 `Σ_Px_P`；对偶给边长 `l_e>=0`，最小化 `Σ_ec_el_e`，且每条 s-t 路径长度至少 1。列数可能指数，但“找最短路径”正是 separation/oracle。

乘权框架从小正长度开始，反复取当前最短路径并推流；边 e 的长度乘上 `1+ε·(增量/c_e)`（或指数等价式），高拥塞边迅速昂贵，算法自动转向替代路径。势函数 `Σ_ec_el_e` 控制总增长，最短路对偶约束给下界；适当初始化、停止并按最大拥塞缩放后，可得到 `(1-O(ε))` 流，迭代数多项式依赖 `ε^{-2}log m`。常数和停止条件是定理的一部分，不能随便删。

课程代码抽取“乘权负载均衡内核”：给显式候选路径，分小批量到当前指数价格最便宜路径，最后按最大容量利用率缩放为可行流；用离散网格枚举同一路径 LP 的小规模 OPT。它展示 oracle 与势函数，但不是完整 Garg–Könemann 参数化实现，因此只断言可行、`ALG<=OPT` 并报告经验 gap。

单商品流还有精确组合算法；乘权价值在多商品、近似最大流和更一般 packing 中更突出。反例：初始权重为 0 会永远不给拥塞边价格信号；加法更新也失去指数势界。

## 精确 60 分钟

- 00–05：写路径 primal/dual。
- 05–25：推演两条共享瓶颈路径的权重增长。
- 25–45：运行 MW 与网格 oracle，画每轮选择。
- 45–55：比较乘法更新与固定最短路。
- 55–60：准确说明代码与完整 FPTAS 的边界。

## 代码实验

脚本随机生成小 packing 矩阵（列=路径、行=边），MW 分配后缩放，网格枚举分数解；断言所有容量约束、并输出 `ALG/OPT_grid`。

## 验收

- 能写路径 LP 对偶。
- 能解释拥塞为何导致价格指数增长。
- 不把教学内核宣称为完整 GK 实现。

## 原始/权威资料

- Garg & Könemann (1998), Faster and simpler algorithms for multicommodity flow: <https://doi.org/10.1109/SFCS.1998.743467>
- Plotkin, Shmoys & Tardos (1995), Fast approximation algorithms for fractional packing and covering: <https://doi.org/10.1287/moor.20.2.257>

