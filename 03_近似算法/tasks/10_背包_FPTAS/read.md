# 第 10 晚：从伪多项式 DP 到 Knapsack FPTAS

## 目标

理解 PTAS/FPTAS 的量词与复杂度；推导利润缩放的 `(1-ε)` 保证；实现按缩放利润的最小重量 DP 并与精确枚举对拍。

## 前置回忆（5 分钟）

0/1 背包：重量 `w_i`、利润 `p_i`、容量 `B`。按重量 DP 是 `O(nB)`；若 `B` 二进制输入，为什么是伪多项式？

## 精读正文（20 分钟）

先删去 `w_i>B` 的物品，令 `Pmax=max p_i`。给定 `0<ε<1`，取 `K=εPmax/n`，缩放利润 `p'_i=floor(p_i/K)`；DP 对每个总缩放利润保存最小重量，复杂度 `O(nΣp'_i)=O(n^3/ε)`，与数值大小无关，故是 FPTAS。

设最优集合 `O`。每件物品向下取整损失小于 `K`，所以由缩放 DP 得到的解 `A` 满足 `p(A)>=Kp'(A)>=Kp'(O)>p(O)-nK=OPT-εPmax`。因最大利润的可行单件本身可选，`Pmax<=OPT`，故 `p(A)>=(1-ε)OPT`。若未先过滤超容量物品，`Pmax<=OPT` 可能为假，证明断裂。

FPTAS 要求运行时间对输入长度和 `1/ε` 都是多项式；PTAS 只要求每个固定 ε 时对输入规模多项式，可能有 `n^{1/ε}`。强 NP-hard 问题通常不可能有 FPTAS（除非 `P=NP`），因为 FPTAS 常可用足够小 ε 恢复精确整数目标。零利润、空实例和浮点 `K` 需谨慎；代码用整数 floor 的等价计算避免累计误差。

## 精确 60 分钟

- 00–05：比较 `B` 与 `log B`。
- 05–25：复写四行误差链，圈出 `Pmax<=OPT`。
- 25–45：运行 FPTAS 与 `2^n` oracle。
- 45–55：画 ε、状态数、经验误差表。
- 55–60：一句话区分 PTAS/FPTAS/伪多项式。

## 代码实验

脚本固定多组 ε，断言可行且 `value >= (1-ε)OPT`。观察 ε 减半时状态数近似翻倍，而答案不会变差（虽因取整并不保证集合嵌套）。

## 验收

- 能推导 `nK=εPmax`。
- 能解释过滤超重物品的证明作用。
- 能给出 FPTAS 的双多项式定义。

## 原始/权威资料

- Ibarra & Kim (1975), Fast approximation algorithms for the knapsack and sum of subset problems: <https://doi.org/10.1145/321906.321909>
- Lawler (1979), Fast approximation algorithms for knapsack problems: <https://doi.org/10.1287/moor.4.4.339>

