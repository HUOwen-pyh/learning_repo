# 第 29 晚：Beyond worst case 的三条轴

## 目标

区分 FPT approximation、fine-grained inapproximability 与 learning-augmented algorithms；实现 Vertex Cover 参数 k 分支与一个“证书基线 + 预测候选”的鲁棒组合器。

## 前置回忆（5 分钟）

FPT 时间写作 `f(k)n^{O(1)}`；它与 PTAS 的参数 ε 有何不同？ETH/SETH 分别排除哪类 SAT 时间？

## 精读正文（20 分钟）

参数化算法把结构参数 k 从 n 的指数中分离。Vertex Cover 若有未覆盖边 `(u,v)`，任何大小 k 解至少选 u/v 之一，分支得到 `T(k)<=2T(k-1)+poly(n)=O(2^k poly(n))`；Buss 规则若 `deg(v)>k` 则必须选 v，否则最多 k 个点各覆盖 k 条边，剩余边数 `>k^2` 即拒绝，产生多项式 kernel。FPT-approximation 则允许近似目标以换更好的 `f(k,ε)` 或处理 W[1]-hard 问题；lossy kernel 明确允许压缩中损失比值。

细粒度下界不仅问“多项式否”，还问能否 `2^{o(n)}`、`n^{k-ε}`。Gap-ETH 假设带常数 satisfiability gap 的 3SAT 不可次指数，特别适合排除快速近似/FPT-AS；每个结论必须注明参数、gap 与随机化版本，不能从普通 ETH 自动替换。

学习增强接收预测但保留 worst-case certificate。最安全的黑盒组合：同时运行有证明的基线 A 与预测候选 P，计算两者真实目标并取较好；Max-Cut 最大化时保证至少 A 的 1/2 OPT（robustness），预测准确时不差于 P（consistency）。它不能保证预测一定加速，且只适用于能快速评价/验证候选。更深模型研究 advice 噪声、distribution shift 与 consistency–robustness Pareto 前沿。

## 精确 60 分钟

- 00–05：写 FPT/PTAS 两种量词。
- 05–25：推 Vertex Cover 分支树与 k² kernel 规则。
- 25–45：运行 FPT 对拍和 Max-Cut 安全组合。
- 45–55：随预测翻转率画质量曲线。
- 55–60：为一个 Gap-ETH 结论列齐参数/时间/比值。

## 代码实验

脚本第一部分 FPT 决策与 `2^n` oracle 对拍；第二部分生成带噪最优 cut 预测，组合器取预测与确定性 1/2 基线的较优者并检查双保证。

## 验收

- 能推导 Vertex Cover 的二叉分支。
- 能区分 ETH 与 Gap-ETH 的用途。
- 能定义学习增强的 consistency 与 robustness。

## 原始/权威资料

- Downey & Fellows, *Parameterized Complexity*: <https://doi.org/10.1007/978-1-4612-0515-9>
- Lokshtanov et al. (2017), Lossy kernelization: <https://doi.org/10.1145/3055399.3055456>
- Attias, Gao & Reyzin (2025), Learning-Augmented Algorithms for Boolean Satisfiability: <https://arxiv.org/abs/2505.06146>
