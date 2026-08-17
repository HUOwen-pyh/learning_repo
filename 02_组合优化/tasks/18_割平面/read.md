# 第 18 晚：割平面、CG/Gomory 与分离

## 学习目标

- 定义 valid inequality：删分数点但不删任何整数可行点。
- 从非负约束组合与取整推导 Chvátal–Gomory cut。
- 理解 cover cut、Gomory mixed-integer cut 与 cut loop。
- 区分“找违反割”的 separation 与“解当前 LP”的 optimization。

## 前置回忆

若 $Ax\le b$ 且乘子 $u\ge0$，则 $uAx\le ub$ 对所有可行点成立。若 $uA$ 的系数为整数且 $x$ 整数，可把右端向下取整。

## 完整精读讲解

例：$2x+y\le4$ 与 $x+2y\le4$。各乘 $1/3$ 后相加得 $x+y\le8/3$；因 $x+y$ 整数，可强化为 $x+y\le2$。LP 最优分数点 $(4/3,4/3)$ 被删除，所有整数点保留。这是 CG cut 的核心。Gomory cut 从单纯形 tableau 的分数行系统化产生；混合整数版本要正确处理连续变量与符号。

0-1 背包约束 $\sum a_jx_j\le b$ 中，若集合 $C$ 的重量和超过 $b$，则不可能全部选择，得到 cover inequality $\sum_{j\in C}x_j\le|C|-1$。最小 cover、lifting 和分离策略决定强度。有效不等式太多时，不预先全部加入，而是解 LP、寻找被当前解违反的割、加入后重解。

纯 cutting-plane 可能数值不稳或收敛慢；现代 MIP 把割与分支结合为 branch-and-cut。割的 efficacy、平行性、稀疏性、全局/局部有效性都影响性能。错误割比弱割更危险：它会悄悄删掉真正最优整数解。因此小实例应枚举所有整数点验证 validity。

复杂度方面，某些分离问题本身 NP-hard；易分离的指数不等式族仍很有价值。椭球法揭示多面体上 separation 与 optimization 的理论等价，但并不意味着工程性能相同。

## 精确 60 分钟

- 00–07：验证一个 valid/invalid inequality。
- 07–19：逐步推导 CG 取整割。
- 19–30：找一个最小 cover 并写 cut。
- 30–39：理解 solve–separate–add 循环。
- 39–53：运行二维 LP 顶点与 CG cut。
- 53–58：枚举整数点验证 cut validity。
- 58–60：写出局部割误当全局割的风险。

## 代码任务

枚举二维 LP 顶点；自动由乘子生成 CG cut；加入后重解并与整数枚举比较。另生成一个 cover cut，对全部 0-1 可行点验证。

## 验收标准

- 原 LP 分数最优值严格大于 IP。
- cut 违反原分数最优点且不删任何整数可行点。
- 加 cut 后本例 LP 值等于 IP。
- 能区分 cut generation 与 cut separation。

## 原始/权威资料

- Gomory 1958 原论文：https://doi.org/10.1007/BF01582234
- Chvátal 1973 Edmonds polytopes and hierarchy：https://doi.org/10.1007/BF01580170
- Balas 1975 Facets of the Knapsack Polytope：https://doi.org/10.1007/BF01580667

