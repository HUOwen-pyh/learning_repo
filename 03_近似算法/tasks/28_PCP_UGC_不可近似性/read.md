# 第 28 晚：从 gap-CSP 到 FGLSS 图——不可近似性的机械接口

## 目标

理解 PCP 把“有解/无解”放大为常数 gap；理解 FGLSS 图如何把局部接受配置变成独立集；准确区分 PCP 定理、平行重复与 UGC 条件阈值。

## 前置回忆（5 分钟）

若一个 verifier 只读随机证明的 q 位，每个随机串有多少局部回答？completeness c 与 soundness s 分别量化什么？

## 精读正文（20 分钟）

PCP 定理 `NP=PCP[O(log n),O(1)]` 意味着 NP 证明可由多项式个随机串、常数 query 检查：YES 有证明总被接受（常见完备性 1），NO 任意证明接受率至多 `s<1`。这给 Max-CSP 的常数 gap；gap-preserving reduction 再传给 Clique、Independent Set、Set Cover 等。

FGLSS 构图：每个“随机串 + 会接受的局部回答”建顶点，权重为该随机串概率；两个不能同时来自同一全局证明的配置相冲突并连边。任意全局证明选出的相容接受配置构成独立集，反之独立集可拼成一致证明，因此最大独立集权重等于 verifier 最大接受率。代码用 3CNF clause 当局部检查：每 clause 的 7 个满足局部赋值为顶点；同 clause 或共享变量取值冲突则连边，最大独立集大小恰等于最多可同时满足 clause 数。

Gap amplification/平行重复降低 soundness，但实例大小也增长；下界常数必须跟踪。UGC（Khot）承诺 Unique Games 的最优值接近 1 或很小难以区分，推出 Max-Cut 的 GW 常数和 Vertex Cover 的 2 等最优阈值；它仍是未证猜想，不能写成无条件定理。Dinur 的组合 gap amplification 给 PCP 定理的新证明，并不证明 UGC。

## 精确 60 分钟

- 00–05：定义 c/s。
- 05–25：画 verifier→FGLSS→独立集对应。
- 25–45：运行 clause 配置图与精确 MIS/MaxSAT 对拍。
- 45–55：给 clause 加权，改为最大权独立集。
- 55–60：分别陈述 P≠NP 条件与 UGC 条件结论。

## 代码实验

脚本枚举每个 3-clause 的 7 个接受配置，建冲突 bitset 图，用带 memo 的分支求 MIS；另枚举全局赋值求 MaxSAT 并断言二者相等。

## 验收

- 能解释独立集为何对应一致局部回答。
- 能区分 completeness 与 soundness。
- 不把 UGC 当已证明事实。

## 原始/权威资料

- Arora et al. (1998), Proof verification and hardness of approximation: <https://doi.org/10.1145/278298.278306>
- Dinur (2007), The PCP theorem by gap amplification: <https://doi.org/10.1145/1236457.1236459>
- Khot (2002), On the power of unique 2-prover 1-round games: <https://doi.org/10.1145/509907.509919>

