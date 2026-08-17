# 第 13 晚：整数规划公式、Big-M 与强建模

## 学习目标

- 建立设施选址的开设变量、分配变量和 linking constraints。
- 比较 aggregate 与 disaggregate 公式的 LP 强度。
- 安全推导 Big-M，处理蕴含、固定成本与对称性。
- 写独立模型检查器并生成小实例真值。

## 前置回忆

0-1 变量 $y_j$ 表示是否开设施，$x_{ij}$ 表示客户 $i$ 是否分给设施 $j$。逻辑“分给 $j$ 则必须开 $j$”最直接是 $x_{ij}\le y_j$。

## 完整精读讲解

无容量设施选址：最小化 $\sum f_jy_j+\sum c_{ij}x_{ij}$；每客户恰分一次 $\sum_jx_{ij}=1$；link 为 $x_{ij}\le y_j$。对固定 $y$，每客户独立选最便宜已开设施，因此子问题可线性时间求解，这也是分解结构。

可把若干 link 聚合为 $\sum_i x_{ij}\le |I|y_j$，整数可行集相同，但 LP 更弱：小分数 $y_j$ 可支撑若干分数分配。强公式通常让 LP 界更接近整数最优，搜索树更小，即使约束更多。模型大小与松弛强度需权衡。

Big-M 表达条件约束时，$M$ 应由变量界严格推得。例如若 $y=1$ 才强制 $a^\top x\le b$，写 $a^\top x\le b+M(1-y)$，安全最小 $M$ 是在变量界内 $a^\top x-b$ 的最大值。任意写 $10^9$ 会导致弱界、缩放差和可行性容差漏洞。若求解器支持 indicator constraint，仍需理解它内部可能转化或分支。

对称性来自可互换设施/车辆：交换标签产生同值解。可用 $y_1\ge y_2\ge\cdots$ 等破缺，但必须确认设施确实同质，否则会删真解。陷阱还包括重复计固定成本、容量单位错、把服务距离与成本混淆、未约束空开的设施。

## 精确 60 分钟

- 00–07：定义集合、参数、变量单位。
- 07–20：写设施选址目标与约束。
- 20–31：比较聚合/分解 linking 的 LP 点。
- 31–40：从上下界推一个最小 Big-M。
- 40–53：运行开设集合枚举与检查器。
- 53–58：添加容量或禁配边。
- 58–60：记录公式强度与规模取舍。

## 代码任务

枚举设施开设子集，对每个子集精确解客户分配；独立核验分配、开设、容量与成本。再比较一个贪心启发式的上界。

## 验收标准

- 模型的每个索引和单位清楚。
- 检查器拒绝“分给未开设施”。
- 枚举最优值与手算一致，并明确它是小规模真值。
- 能给出聚合 link 更弱的具体分数点。

## 原始/权威资料

- Williams, Model Building in Mathematical Programming：https://www.wiley.com/en-us/Model+Building+in+Mathematical+Programming%2C+5th+Edition-p-9781118443330
- Vielma 2015, Mixed Integer Linear Programming Formulation Techniques：https://doi.org/10.1137/130915303
- SCIP 建模与约束处理官方文档：https://scipopt.org/doc/html/

