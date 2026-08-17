# 第 27 晚：输入顺序成为对手——competitive analysis

## 目标

区分离线近似比与在线竞争比；证明 deterministic ski rental 为 2-competitive；理解随机化、对手模型及 online set cover/facility location 的入口。

## 前置回忆（5 分钟）

每天租赁成本 1，一次购买成本 B，不知道共使用 D 天。离线 OPT 是什么？一个在线算法能否在第 1 天判断 D？

## 精读正文（20 分钟）

在线算法按到达顺序不可撤销决定。`c`-competitive 常指 `ALG(σ)<=c·OPT(σ)+β` 对所有序列 σ；β 允许处理固定启动成本。Ski rental 在租满 B 天前一直租，下一天买（约定实现细节后总成本不超过 `2B-1`）。若 D<B，ALG=D=OPT；若 D>=B，ALG<=2B-1<2OPT，故 2-competitive。确定性下界由对手在你买前停止或让季节继续构成。

随机买入时刻可把 oblivious-adversary 竞争比降到 `e/(e-1)`；必须注明对手是否看见随机位。在线与近似可叠加：每个时刻问题本身 NP-hard，算法可能同时有近似损失与信息损失。Online Set Cover 的多对数竞争算法用分数权重/随机阈值；Meyerson online facility location 以与连接距离相关的概率开设施，得到期望对数级竞争。

学习增强算法加入预测（如预计 D），评价两条轴：预测准确时 consistency 与任意错误时 robustness。直接“完全相信预测”可能一致但无鲁棒界；第 29 晚实现安全组合。代码穷举所有 D 验证 ski rental 的逐序列保证，并模拟随机策略的期望。

## 精确 60 分钟

- 00–05：写离线 OPT。
- 05–25：分 D<B/D>=B 证明 2。
- 25–45：运行逐 D 对拍与随机策略模拟。
- 45–55：设计一个自适应对手击败天真随机策略。
- 55–60：对比 approximation ratio 与 competitive ratio 的基准。

## 代码实验

确定性策略无概率断言；随机策略使用离散化的经典指数分布并只报告经验比，不把 Monte Carlo 当定理。

## 验收

- 能写 competitive ratio 的序列量词。
- 能解释 deterministic 2 下界的对手。
- 能区分 oblivious 与 adaptive adversary。

## 原始/权威资料

- Karlin et al. (1994), Competitive randomized algorithms for nonuniform problems: <https://doi.org/10.1007/BF02574699>
- Alon et al. (2003), The online set cover problem: <https://doi.org/10.1145/780542.780558>
- Meyerson (2001), Online facility location: <https://doi.org/10.1109/SFCS.2001.959917>

