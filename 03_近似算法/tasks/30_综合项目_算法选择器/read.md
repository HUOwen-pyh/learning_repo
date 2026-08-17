# 第 30 晚：综合项目——从实例结构到可审计保证

## 目标

把 29 晚技术组织成算法选择器；对每次输出同时生成可行性证书、下界/上界和声明条件；学会拒绝不满足前提的实例。

## 前置回忆（5 分钟）

列一个近似结果必须报告的五项：问题方向、前提、算法值、bound/certificate、比值。想一想 metric TSP 若三角不等式不成立应做什么。

## 精读正文（20 分钟）

真实系统不能只按问题名分派算法，还要验证结构：Vertex Cover 区分带权/无权；TSP 检查对称、非负、三角不等式；k-center 检查 k 范围；submodular 只能在 oracle/已知结构下相信次模性；随机算法记录 seed 与成功概率。

报告采用“算法值 + 独立 certificate”而非自我宣称。最小化中 matching/LP/MST/对偶给下界 LB，并证 `ALG<=αLB`；最大化中总边权、LP/SDP 或精确测试 oracle 给上界 UB，并证 `ALG>=ρUB`。若 certificate 只给 `LB<=OPT` 却无法证 `ALG<=αLB`，不能报告 α。小规模 exact oracle 用于 CI 对拍，大实例关闭。

选择策略示例：无权 Vertex Cover→极大匹配 2；metric k-center→farthest-first 2；单调 coverage+基数→边际贪心 `1-1/e`；Knapsack 有 ε→FPTAS；Max-Cut→确定性 1/2，若可用 SDP optimizer 再升级 GW。工程上还要把数值容差、超时、内存和不可行输入写进 schema。

前沿算法不等于默认更好：`3/2-ε` metric TSP 的 ε 极小且实现复杂；学习策略可能经验优越却无分布外证书。推荐双轨：始终保留 certified baseline，同时以插件式候选竞争，只有验证后的更好可行解才替换基线。

## 精确 60 分钟

- 00–05：写五项报告字段。
- 05–25：阅读选择表，给每分支标前提和 certificate。
- 25–45：运行综合脚本，看 JSON 风格报告与随机 CI。
- 45–55：新增 double-tree TSP 分支及三角检查。
- 55–60：选一个研究前沿写“可部署前还缺什么”。

## 代码实验

`practice.py` 实现三个分支的统一 `solve`：Vertex Cover、k-center、Maximum Coverage。每个报告含算法、保证、目标值、证书值和已验证前提；随机小实例由 exact oracle 做 CI。

## 验收

- 任给分支都能说出保证方向与证书。
- 前提失败时会拒绝而不是静默输出保证。
- 能区分生产算法、测试 oracle 和研究候选。

## 原始/权威资料

- Williamson & Shmoys（设计与证明总纲）：<https://www.designofapproxalgs.com/book.pdf>
- Johnson (1974), Approximation algorithms for combinatorial problems: <https://doi.org/10.1016/S0022-0000(74)80044-9>
- Karlin, Klein & Oveis Gharan (2021)（前沿落地取舍示例）：<https://doi.org/10.1145/3406325.3451009>

