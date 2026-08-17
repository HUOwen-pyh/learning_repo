# 第160晚：Inspect 评分与 τ-bench

## 目标与前置

- 目标：区分逐步轨迹相似度、数据库终态正确性与 pass^k 稳定性。
- 前置：第159晚、概率基础、事务状态。

## 计入 60 分钟的必读

| 分钟 | 材料 | 版本 | 精确范围 | 问题 |
|---:|---|---|---|---|
| 8 | [Inspect Scoring](https://inspect.aisi.org.uk/scoring.html) | checked_at 2026-08-15 | Scorer、Metric、Model-graded scoring | scorer 与 metric 为何分开？ |
| 12 | [τ-bench: A Benchmark for Tool-Agent-User Interaction](https://arxiv.org/html/2406.12045#S3) | arXiv:2406.12045v1 / ICLR 2025 | §3 的 Reward 与 “Pass^k metric” 两段（PDF p.4），尤其组合数无偏估计式 | 为什么一次成功掩盖不稳定性？ |

## 阅读导引

分别记录最终数据库约束、用户沟通约束和工具调用轨迹。重点推导 pass^k 是“k 次全部成功”的严格稳定性指标，而不是“至少一次成功”。

## 核心推导

任务 i 若运行 `n_i` 次、其中 `c_i` 次成功，则论文给出的经验无偏估计是 `pass^k = (1/N) Σᵢ C(c_i,k)/C(n_i,k)`（要求 `n_i≥k`）：它等价于从该任务的 n 次观测中均匀选 k 次，估计“k 次全部成功”的概率。仅当 `n_i=k` 时，该项才退化为全部 k 次成功的 0/1 指示量；不能固定取“前 k 次”。只有额外假设所有任务、trial 独立同分布且成功率同为 p 时，其总体期望才退化为 p^k。终态 scorer 应检查业务不变量；轨迹可作为诊断，但存在多条不同且同样正确的路径。

## 工业联系与事实标签

- [THEOREM] 对固定的逐任务 trial 矩阵且 `k+1≤min n_i`，组合数估计满足 pass^(k+1)≤pass^k；逐任务比值递推因子为 `(c_i-k)/(n_i-k)≤1`（`c_i<k` 时两项均为 0）。
- [EMPIRICAL] τ-bench 的结果依其领域、用户模拟器、策略与重复运行协议。
- [INFERENCE] 高风险自动化应报告重复运行尾部失败，而非只报平均分。
- [OPEN] 模拟用户和真实用户行为之间的分布差距无法由 benchmark 自身消除。

## 严格 60 分钟

- 0–5：写两个终态不变量；5–25：必读；25–48：运行 scorer；48–55：比较 pass@k 与 pass^k；55–60：解释一次成功为何不够。

## 验收

正确终态、错误余额、`n>k` 非平凡组合数、`n<k` 拒绝与 k=0 约定均有断言；能从三项任务各自的重复结果手算 pass^2。

## 可选延伸

阅读 τ-bench 数据生成附录，不计时。
