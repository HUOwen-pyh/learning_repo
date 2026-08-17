# 第 23 晚：多面体组合、facet 与分离—优化

## 学习目标

- 区分 valid inequality、face、facet 与完整线性描述。
- 用 TSP subtour inequality 做小规模 separation。
- 理解“指数多约束 + 多项式分离”仍可算法化。
- 连接多面体强度、branch-and-cut 与扩展公式。

## 前置回忆

多面体 $P=\operatorname{conv}(X)$ 是所有整数可行解的凸包。有效不等式 $a^\top x\le b$ 定义 face；若该 face 维数恰为 $\dim(P)-1$，它是 facet。

## 完整精读讲解

理想公式的 LP 可行域就是 $\operatorname{conv}(X)$，所有顶点整数。facet 是在当前变量空间中不可轻易加强的“最大维边界”，但一个公式只有很多 facet 不代表计算一定快；系数、退化和对称也重要。扩展公式在更高维引入变量，投影回原空间，可用较少约束描述同一集合。

TSP degree 方程允许多个不相交环。对任意非空真子集 $S$，巡回至少两次跨越割，故 $x(\delta(S))\ge2$。给分数解 x，separation 要找容量小于 2 的割；这是全局最小割问题，可多项式求。教学代码枚举子集是 $O(2^n n^2)$，只为显示证书。

Grötschel–Lovász–Schrijver 的理论说明，对有理多面体，强 separation oracle 与线性 optimization 在多项式意义下等价（借助椭球法）。含义是无需显式列出所有不等式；不意味着实际一定用椭球，也不意味着 separation 总是容易。匹配 blossom 可分离，TSP 的某些强割族分离则可能困难。

facet 证明常分两步：证明不等式有效；构造足够多仿射独立的取等可行点。陷阱：只找到违反点就声称 facet、把 degree 等式计入维数错误、无向边重复计数、只查连通分量而漏分数小割、局部 cut 离开节点后仍全局使用。

## 精确 60 分钟

- 00–07：在二维区分 face/facet/冗余约束。
- 07–19：推导 TSP subtour inequality。
- 19–30：检查“两三角形”分数/整数 2-factor。
- 30–39：理解 min-cut separation 与理论等价。
- 39–53：运行子集分离并输出最违反割。
- 53–58：枚举所有巡回验证 inequality。
- 58–60：说明有效不等式不一定是 facet。

## 代码任务

构造满足每点 degree=2 但由两个环组成的 x；枚举真子集找到最小 cut；对所有小型 Hamiltonian tours 验证生成的不等式有效。

## 验收标准

- degree checker 通过而 subtour checker 拒绝。
- 输出 S、cut value 与具体跨割边。
- 所有 Hamiltonian tours 的 cut 至少 2。
- 能解释生产版为何应调用 min-cut 而非枚举子集。

## 原始/权威资料

- Dantzig, Fulkerson & Johnson 1954 TSP cutting planes：https://doi.org/10.1287/opre.2.4.393
- Grötschel, Lovász & Schrijver, Geometric Algorithms：https://doi.org/10.1007/978-3-642-78240-4
- Fiorini et al. 2015 TSP 扩展复杂度：https://doi.org/10.1145/2716307

