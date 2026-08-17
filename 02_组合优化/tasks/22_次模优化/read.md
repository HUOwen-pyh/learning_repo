# 第 22 晚：次模函数、最大覆盖与 $1-1/e$

## 学习目标

- 用边际递减定义/验证次模性。
- 对基数约束下单调次模最大化实现 greedy。
- 推导 $1-(1-1/k)^k\ge1-1/e$ 保证。
- 了解非单调、拟阵约束与次模最小化的不同算法边界。

## 前置回忆

集合函数边际增益 $\Delta(e\mid S)=f(S\cup\{e\})-f(S)$。覆盖函数 $f(S)=|\cup_{i\in S}A_i|$；当已覆盖更多时，新集合能带来的新元素不会变多。

## 完整精读讲解

次模性可写：若 $A\subseteq B$ 且 $e\notin B$，则 $\Delta(e\mid A)\ge\Delta(e\mid B)$；等价于 $f(A)+f(B)\ge f(A\cup B)+f(A\cap B)$。它是离散“凹性”。最大覆盖、影响力扩散期望、传感器信息增益在适当条件下次模。

对规范化 $f(\varnothing)=0$、非负、单调次模函数，在最多选 k 个元素时，每轮选最大边际。设当前 $S_i$，最优集 OPT 的 k 个元素总边际足以覆盖剩余差距，因此至少一个元素边际不小于 $(f(OPT)-f(S_i))/k$。差距每轮乘至多 $(1-1/k)$，k 轮后得
$f(S_k)\ge[1-(1-1/k)^k]f(OPT)\ge(1-1/e)f(OPT)$。

这个常数在 oracle 模型下本质紧。若有 costs/knapsack constraint，要用密度、枚举大项或连续贪心；拟阵约束下简单 greedy 只有 1/2，continuous greedy 可达 $1-1/e$。非单调最大化需要 double greedy 等；无约束次模最小化是多项式可解但算法更深。

实现陷阱：缓存覆盖集合后原地修改导致候选边际串扰、tie-break 不稳定、函数实际不单调却套证明、Monte Carlo 估计噪声使边际次序偏差、用训练集覆盖评估泛化。

## 精确 60 分钟

- 00–07：手算覆盖函数四个边际。
- 07–18：验证两种次模定义等价直觉。
- 18–31：逐步推导 greedy 残差递推。
- 31–39：比较基数、背包、拟阵约束。
- 39–53：运行 greedy、穷举与次模检查。
- 53–58：构造 tie 与非单调反例。
- 58–60：口述保证成立的四个前提。

## 代码任务

实现带权最大覆盖的 lazy/普通 greedy；小实例穷举 OPT；枚举 $A\subseteq B,e\notin B$ 验证边际递减，并核验保证。

## 验收标准

- 返回集合大小不超过 k，价值独立重算。
- 对全部小集合检查通过次模性与单调性。
- greedy 值达到理论下界，且不声称每例都最优。
- 能指出简单 greedy 在拟阵约束下的保证变化。

## 原始/权威资料

- Nemhauser, Wolsey & Fisher 1978：https://doi.org/10.1007/BF01588971
- Calinescu et al. 2011 continuous greedy：https://doi.org/10.1137/080733991
- Buchbinder et al. 2015 double greedy：https://doi.org/10.1137/140957543

