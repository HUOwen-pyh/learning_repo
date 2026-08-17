# 第 11 晚：List Scheduling、LPT 与 makespan 下界

## 目标

证明相同并行机 `P||Cmax` 的 list scheduling 是 `2-1/m` 近似；理解 LPT 的 `4/3-1/(3m)` 改进来自“关键作业足够小”；用精确分配 oracle 对拍。

## 前置回忆（5 分钟）

对作业时长 `p_j`、`m` 台相同机器，写出两个下界：`OPT>=Σp_j/m` 与 `OPT>=max p_j`。什么是完成最晚的关键作业？

## 精读正文（20 分钟）

List Scheduling 按任意顺序，把下一作业放到当前负载最小机器。设最终 makespan 的关键作业 `j` 时长 `p_j`，开始时刻 `s_j`。放置它时每台负载都至少 `s_j`，所以 `m s_j <= Σ_{k≠j}p_k`。于是
`Cmax=s_j+p_j <= (Σp)/m +(1-1/m)p_j <= OPT+(1-1/m)OPT=(2-1/m)OPT`。

LPT 先按非增时长排序。若关键作业是每台前三个以内的大作业，可用结构论证得到最优；否则它在本机至少第 4 个，结合“若 `p_j>OPT/3` 则每机最多放两个这类作业”的交换论证，得到 `p_j<=OPT/3`，代回精化链得 `4/3-1/(3m)`。完整证明需处理最小反例与作业位置，不能仅把 `p_j<=OPT/3` 当作无条件事实。

实现用最小堆可达 `O(n log m)`。反例意识：LPT 通常更好但不保证得到 OPT；若有 release time、precedence 或 unrelated machines，上述“最小负载”和平均下界不足，保证不能照搬。精确 oracle 枚举 `m^n` 个分配，仅用于小规模。

## 精确 60 分钟

- 00–05：写两个下界。
- 05–25：复写 LS 证明，并标出关键作业。
- 25–45：运行任意序与 LPT，对拍 OPT。
- 45–55：枚举寻找 LPT 非最优最小实例。
- 55–60：口述 LPT 改进所需结构。

## 代码实验

脚本穷举小整数作业，断言 LS 与 LPT 两个经典界；输出观察到的最坏比。更换 tie-breaking 后界仍成立。

## 验收

- 能解释 `ms_j` 为何不超过其他作业总量。
- 不无条件声称关键作业 `<=OPT/3`。
- 能给出堆实现复杂度。

## 原始/权威资料

- Graham (1966), Bounds for certain multiprocessing anomalies: <https://doi.org/10.1002/nav.3800130211>
- Graham (1969), Bounds on multiprocessing timing anomalies（LPT 界）：<https://doi.org/10.1137/0117039>

