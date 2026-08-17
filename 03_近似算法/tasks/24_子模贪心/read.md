# 第 24 晚：从 coverage 到一般单调次模 value oracle

## 目标

掌握次模性的 diminishing returns 与集合不等式定义；将第 03 晚证明提升到任意单调次模函数；实现 concave-over-modular 价值并自动验证次模性。

## 前置回忆（5 分钟）

两种定义：`A⊆B, e∉B` 时 `f(A+e)-f(A)>=f(B+e)-f(B)`；等价的 `f(A)+f(B)>=f(A∪B)+f(A∩B)`。覆盖函数为何满足？

## 精读正文（20 分钟）

在基数约束 `|S|<=k` 下，每步选最大边际 `Δ(e|S)`。对最优 O，次模性给
`OPT-f(S_i) <= f(S_i∪O)-f(S_i) <= Σ_{e∈O\S_i}Δ(e|S_i)`；至多 k 项，所以贪心边际至少缺口/k。递推得到 `f(S_k)>=[1-(1-1/k)^k]OPT >=(1-1/e)OPT`。

本晚 value oracle 不是集合并，而是 concave-over-modular：有多个特征 h，元素 e 提供非负量 `a_he`，`f(S)=Σ_h w_h sqrt(Σ_{e∈S}a_he)`。凹函数复合非负可加量产生 diminishing returns；代码还穷举 A⊆B 与 e 检查。若用凸函数平方，边际随已有量增大，变成超模，贪心证明断裂。

value-oracle 模型下朴素调用次数 `O(nk)`；lazy greedy 用优先队列利用边际只降，保持同样选择（并列除外），但最坏 oracle 次数未必改善。若函数非单调，继续加元素可能降低值，`1-1/e` 结论不适用，需要 double greedy、随机化或连续方法。

## 精确 60 分钟

- 00–05：写两种次模定义。
- 05–25：从 union 上界推缺口递推。
- 25–45：运行一般 oracle、次模枚举、OPT 对拍。
- 45–55：把 sqrt 改平方，捕获最小反例。
- 55–60：说出单调性与次模性各用在哪里。

## 代码实验

脚本生成非负 feature 矩阵，穷举验证函数单调次模；贪心与组合 OPT 对拍并检查有限 k 精确界。

## 验收

- 能写出 `f(S∪O)-f(S)` 的边际和上界。
- 能给出 concave-over-modular 的直觉。
- 能区分非单调次模问题。

## 原始/权威资料

- Nemhauser, Wolsey & Fisher (1978): <https://doi.org/10.1007/BF01588971>
- Krause & Golovin, Submodular Function Maximization（综述章节）：<https://doi.org/10.1016/B978-0-444-53759-8.00003-9>

