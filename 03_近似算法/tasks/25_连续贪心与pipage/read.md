# 第 25 晚：Multilinear Extension、连续贪心与 pipage rounding

## 目标

把离散次模函数扩展到 `[0,1]^n`；理解连续贪心的梯度方向；实现 coverage 的精确 multilinear extension 与 pipage 舍入。

## 前置回忆（5 分钟）

独立以概率 `x_i` 选择元素得到随机集 R(x)，定义 `F(x)=E[f(R(x))]`。对 coverage，某个 universe 元素未覆盖概率是多少？

## 精读正文（20 分钟）

Coverage 的扩展为
`F(x)=Σ_e w_e[1-Π_{i:e∈S_i}(1-x_i)]`。
在 uniform-matroid polytope `Σx_i<=k` 上，continuous greedy 从 x=0 出发，时间 t∈[0,1] 每刻选 polytope 内最大化 `<v,∇F(x)>` 的方向（基数情形选 k 个最大偏导），令 `dx/dt=v`。次模性给微分不等式 `dF/dt>=OPT-F`，解得 `F(x(1))>=(1-1/e)OPT`。

最后需相关舍入。Pipage rounding 选两个分数坐标 i,j，沿 `x_i+x_j` 不变的线移动到某个端点。对次模 multilinear F，这条线是凸的（混合二阶偏导非正，换成 `(+δ,-δ)` 后二阶为 `-2∂²F/∂x_i∂x_j>=0`），所以两个端点至少一个 F 不低于当前值；反复得到 0/1 向量并保持基数。

代码用有限步 Euler 连续贪心，随后精确评估两个 pipage 端点；离散步引入 `O(1/T)` 型误差，所以实验用宽松 `(1-1/e-0.03)` 检查，而核心舍入断言是每步 F 不降。一般 matroid 的方向需最大权独立集 oracle；swap rounding 提供期望保持与负相关性质。

## 精确 60 分钟

- 00–05：推 coverage 的 F。
- 05–25：解微分不等式并推 pipage 线凸性符号。
- 25–45：运行离散 continuous greedy + pipage。
- 45–55：改变步数 T，记录误差和梯度调用数。
- 55–60：解释独立舍入为何可能违反恰好 k。

## 代码实验

脚本解析计算 F 与梯度，连续贪心后保持 `Σx=k`，pipage 每步取更好端点；最终集合与组合 OPT 对拍。

## 验收

- 能写 coverage multilinear 公式。
- 能说明 pipage 方向的凸性符号。
- 能区分分数保证与可行整数舍入。

## 原始/权威资料

- Calinescu, Chekuri, Pál & Vondrák (2011), Maximizing a monotone submodular function subject to a matroid constraint: <https://doi.org/10.1137/080733991>
- Ageev & Sviridenko (2004), Pipage rounding: <https://doi.org/10.1023/B:JOCO.0000038913.96607.c2>
