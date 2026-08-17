# 第 26 晚：随机优化、SAA 与样本外评估

## 学习目标

- 区分先验决策、随机变量、recourse 与情景。
- 建立两阶段期望成本模型和 Sample Average Approximation（SAA）。
- 分开训练样本最优、真实/大样本评估与统计误差。
- 识别 value of stochastic solution、EVPI 和过拟合。

## 前置回忆

报童问题先订购 q，再观察需求 D；缺货和剩余的成本不同。决策 q 不能依赖尚未观察的 D，否则发生 anticipativity 泄漏。

## 完整精读讲解

两阶段随机规划写作
$\min_{x\in X} c^\top x+\mathbb E_\xi[Q(x,\xi)]$。
第一阶段 x 在信息揭示前决定；第二阶段 Q 可依赖情景。有限离散分布可展开 extensive form，并用 nonanticipativity 让相同历史的决策一致。

SAA 用独立样本 $\xi_1,\dots,\xi_N$ 把期望替成均值。固定有限决策集下随 N 增大通常一致，但一个样本上的最优目标有 selection bias：因为在同一噪声上挑了最小者，不能当无偏的样本外性能。正确流程是训练样本选 x，独立验证样本估计性能，多次 replication 报均值、标准误/置信区间。

报童成本可写采购 $cq+h(q-D)_++p(D-q)_+$。在连续理想模型中 critical fractile 给分位数；离散/有界 q 可直接枚举。风险中性期望会忽视尾部，可改用 CVaR、多阶段场景树或 chance constraint，但每种风险度量回答不同问题。

EV 解把随机量替成均值；EEV 是把 EV 决策放回随机模型的表现；VSS=EEV−RP（最小化）量化建随机模型的价值。EVPI=RP−WS，其中 wait-and-see 允许完美预知，是信息价值上界。

陷阱：用同一随机样本训练和汇报、没有固定种子、情景概率不归一、把均值需求的最优当期望成本最优、测试样本过小、忽略置信区间、让第一阶段偷看情景。

## 精确 60 分钟

- 00–07：标注决策发生与信息揭示时间线。
- 07–19：写报童情景成本与期望。
- 19–30：理解 SAA、selection bias、独立验证。
- 30–39：计算 EV/EEV/VSS/EVPI 的方向。
- 39–53：运行多个 SAA replication。
- 53–58：比较 N=10 与 N=200 的分布。
- 58–60：写下训练/验证随机种子。

## 代码任务

已知小离散分布用于真值；从中采样训练集求 SAA q；用真实期望作样本外评价；重复多次，报告 q 分布、regret 均值与 95% 均值区间。

## 验收标准

- 第一阶段 q 对所有情景相同。
- 真实期望由概率加权独立重算。
- 训练与评价分离，结果可由种子复现。
- 大样本平均 regret 通常下降，但不把单次非单调当失败。

## 原始/权威资料

- Shapiro, Dentcheva & Ruszczyński, Lectures on Stochastic Programming：https://doi.org/10.1137/1.9781611973433
- Kleywegt, Shapiro & Homem-de-Mello 2002 SAA：https://doi.org/10.1137/S1052623499363220
- Birge & Louveaux, Introduction to Stochastic Programming：https://doi.org/10.1007/978-1-4614-0237-4

