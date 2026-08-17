# 第 16 晚：对偶增长与 frequency-f Set Cover

## 目标

从覆盖 LP 推出 packing 对偶；实现“涨价直到集合紧”的 primal-dual；用弱对偶证明频率 `f` 近似，并与第 13 晚阈值舍入对照。

## 前置回忆（5 分钟）

原始 LP 是 `min Σ_S c_Sx_S`、`Σ_{S∋e}x_S>=1`。试写对偶：每个元素变量 `y_e>=0`，每个集合的预算约束是什么？

## 精读正文（20 分钟）

对偶为 `max Σ_e y_e`，约束每集合 `Σ_{e∈S}y_e<=c_S`。把 `y_e` 看成元素愿意支付的价：选一个未覆盖元素 e，同时增加 `y_e`，直到某个包含 e 的集合预算刚好用满（tight），选该集合；重复到覆盖全部元素。所有增加量取当前最小 slack，故始终对偶可行；每个被选集合都 tight。

于是
`ALG=Σ_{S chosen}c_S=Σ_{S chosen}Σ_{e∈S}y_e
 =Σ_e y_e·(# chosen sets containing e)
 <=fΣ_e y_e<=fOPT`。
最后一步是弱对偶。与 LP 阈值舍入不同，这里无需先求完整 LP 最优；算法同步构造原始整数解和对偶证书。reverse-delete 可删冗余集合，通常改善结果，但频率证明不依赖它。

若一次出现多个 tight 集合，只选能覆盖当前 e 的一个即可；所有后续所选仍 tight。负成本会破坏 LP 合理性，零成本集合应预处理。无集合包含未覆盖元素时原问题不可行。代码用 `Fraction` 精确维护 slack，并让穷举 OPT 验证“对偶值<=OPT”。

## 精确 60 分钟

- 00–05：从原始写对偶。
- 05–25：逐行复现成本重排与 f 次计数。
- 25–45：运行对偶增长，查看 y 与 tight 约束。
- 45–55：实现 reverse-delete 并确保覆盖不坏。
- 55–60：比较 threshold rounding 与 primal-dual 所需输入。

## 代码实验

脚本随机生成频率有界实例，返回 picked 与对偶 y；断言对偶可行、所选集合 tight、`ALG<=f·dual<=f·OPT`。

## 验收

- 能写出覆盖 LP 的对偶。
- 能解释每个 y 最多被收费 f 次。
- 能说明弱对偶在何处使用。

## 原始/权威资料

- Bar-Yehuda & Even (1981), A linear-time approximation algorithm for weighted vertex cover: <https://doi.org/10.1016/0022-0000(81)90020-1>
- Goemans & Williamson (1995), The primal-dual method for approximation algorithms and its application to network design: <https://doi.org/10.1007/BF01585996>

