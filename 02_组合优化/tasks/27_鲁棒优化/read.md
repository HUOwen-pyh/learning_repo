# 第 27 晚：鲁棒优化、不确定集与预算鲁棒

## 学习目标

- 区分随机期望、chance constraint 与 worst-case 鲁棒目标。
- 用 box/polyhedral/ellipsoidal 不确定集表达信息。
- 计算 Bertsimas–Sim $\Gamma$ 预算不确定下的最坏偏差。
- 画出 robustness–performance 曲线并做样本外压力测试。

## 前置回忆

若选择项目集合 S，名义收益是 $\sum_{i\in S}\bar p_i$，每项最多下跌 $d_i$。box uncertainty 假设所有选中项可同时发生最大下跌，可能非常保守。

## 完整精读讲解

鲁棒优化要求一个决策对不确定集 $U$ 内所有参数可行/评价最坏情形。它不需要完整概率分布，但结论只和所选 U 一样可信。箱集易解释却常把所有坏事同时发生；椭球集连接二阶锥；多面体集常保留 LP/MIP 可解性。

Bertsimas–Sim budget uncertainty 用 $\Gamma$ 限制同时达到最大偏差的系数数目。对已选项目，最坏收益等于名义和减去最大的 $\lfloor\Gamma\rfloor$ 个偏差，再减 $\Gamma-\lfloor\Gamma\rfloor$ 乘下一个偏差。$\Gamma=0$ 是名义模型，$\Gamma=n$ 是 box。其 robust counterpart 可线性化，不必枚举所有对手。

鲁棒解的名义性能通常下降，换来压力情景改善；“price of robustness”应在多组 $\Gamma$ 和样本外扰动上展示，而不是只选一个漂亮参数。adjustable robust optimization 允许部分决策观察不确定性后调整，但完全可调规则难求，常限制为 affine decision rules。

distributionally robust optimization（DRO）让概率分布落在 ambiguity set 中，再取最坏期望；它介于精确分布随机规划与点集 worst-case 之间。Wasserstein、moment sets 是研究入口。陷阱：U 未按业务/统计校准、把鲁棒目标称概率保证、$\Gamma$ 单位解释错、double-count 偏差、只报 worst-case 不报名义损失。

## 精确 60 分钟

- 00–07：比较随机、鲁棒、DRO 的量词。
- 07–19：写 box 与 budget uncertainty。
- 19–30：手算分数 $\Gamma$ 的最坏偏差。
- 30–39：理解 robust counterpart/对手问题。
- 39–53：枚举选择集并画文本 frontier。
- 53–58：随机压力测试名义与鲁棒方案。
- 58–60：声明不确定集的业务含义。

## 代码任务

从 7 个项目恰选 3 个；对多个 $\Gamma$ 枚举 robust optimum；用独立对手枚举验证整数 $\Gamma$ 公式，并检查最优 worst-case 值随 $\Gamma$ 不增。

## 验收标准

- 决策满足组合约束，最坏收益独立重算。
- $\Gamma=0$ 与名义模型一致，$\Gamma=n$ 与全偏差一致。
- 报告 nominal 与 robust value，不混为同一指标。
- 能解释分数 $\Gamma$ 的“一个部分偏差”。

## 原始/权威资料

- Soyster 1973 线性鲁棒模型：https://doi.org/10.1287/opre.21.5.1154
- Bertsimas & Sim 2004 Price of Robustness：https://doi.org/10.1287/opre.1030.0065
- Ben-Tal, El Ghaoui & Nemirovski, Robust Optimization：https://doi.org/10.1515/9781400831050
- Rahimian & Mehrotra 2019 DRO 综述：https://doi.org/10.48550/arXiv.1908.05659

