# 第 11 晚：LP 对偶、Farkas 与互补松弛

## 学习目标

- 从标准形正确写出对偶并处理约束/变量符号。
- 用弱对偶产生界，用强对偶认证 LP 最优。
- 用互补松弛从一侧解恢复另一侧结构。
- 区分最优证书与 Farkas 不可行证书。

## 前置回忆

第 10 晚 primal 为最大化且约束 $Ax\le b,x\ge0$ 时，dual 是 $\min b^\top y$，满足 $A^\top y\ge c,y\ge0$。先用逐项乘法证明任意可行 $x,y$ 有 $c^\top x\le b^\top y$。

## 完整精读讲解

弱对偶链为 $c^\top x\le y^\top Ax\le y^\top b$。因此 primal 可行值是下界、dual 可行值是上界（针对最大化）。强对偶称只要 LP 有有限最优值，两侧最优值相等。算法给出的两个可行向量若目标相等，无需知道内部 pivot 过程就能认证最优。

互补松弛把等值条件逐项化：$y_i(b_i-a_i^\top x)=0$，以及 $x_j((A^\top y)_j-c_j)=0$。正的 dual 变量对应紧 primal 约束；正的 primal 变量对应紧 dual 约束。它不说“紧约束一定有正乘子”，退化时可能两者都为零。

Farkas 引理给二择一：线性系统有解，或存在一个乘子组合导出矛盾，但不能二者皆有。它是 LP 不可行状态的证书，也是 Benders 可行性割和求解器 infeasibility ray 的基础。无界 primal 通常对应 dual 不可行，但“primal 不可行”并不自动说明 dual 无界，需按对偶状态表判断。

符号规则是高频陷阱：等式约束对应自由 dual 变量；自由 primal 变量对应等式 dual 约束；min/max 和不等号方向必须统一后再机械转置。数值求解中 primal residual、dual residual 和 duality gap 都要在容差内，打印为相同的小数不等于严格证书。

## 精确 60 分钟

- 00–07：手推弱对偶链。
- 07–20：从 primal 写 dual，做两次符号变体。
- 20–31：逐项推导互补松弛。
- 31–39：理解 Farkas 二择一与状态表。
- 39–53：运行有理数 primal/dual 顶点枚举。
- 53–58：从 primal 活跃集恢复 dual。
- 58–60：写出一条错误的“紧则正”陈述并纠正。

## 代码任务

分别枚举二维 primal 与三变量 dual 的顶点；核验可行性、目标相等和互补松弛；把任何一个对偶约束改松，观察证书失效。

## 验收标准

- 能不用口诀、由拉格朗日上界推导 dual。
- primal/dual 都有独立可行性检查。
- 目标严格相等且逐项互补乘积为零。
- 能解释不可行、无界、最优三类状态的证书。

## 原始/权威资料

- von Neumann 1947 对偶思想历史：https://doi.org/10.1515/9781400881635-002
- Bertsimas & Tsitsiklis 线性优化教材：https://www.athenasc.com/linoptbook.html
- MOSEK 对偶与锥优化建模手册：https://docs.mosek.com/modeling-cookbook/duality.html

