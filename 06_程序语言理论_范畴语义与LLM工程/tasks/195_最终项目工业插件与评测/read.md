# 第195晚：最终项目——工业插件与评测

## 目标与前置

- 目标：为策略、审计、成本、重试分别做插件，并用终态/稳定性/泄漏指标评测。
- 前置：第160、168、185晚。

## 计入 60 分钟的必读

| 分钟 | 材料 | 版本 | 精确范围 | 问题 |
|---:|---|---|---|---|
| 10 | [Harness tool events](https://github.com/deepseek-ai/deepseek-harness/blob/47f943859bef60e4160492346772ded9b24f765a/packages/core/tools/src/index.ts#L127-L196) | Harness 47f943859bef60e4160492346772ded9b24f765a | path packages/core/tools/src/index.ts；L127–196；symbols ToolEvents guard/pre/post/finalize/result；checked_at 2026-08-15 | 每个横切关注点应插在哪个 checkpoint？ |
| 10 | [τ-bench paper](https://arxiv.org/html/2406.12045#S3) | arXiv:2406.12045v1 / ICLR 2025 | §3 的 “Pass^k metric” 段及公式：每任务 `C(c,k)/C(n,k)`，再跨任务平均 | 为什么平均 reward 不能替代逐任务稳定性？ |

## 阅读导引

策略只作 allow/deny；审计只观察；成本插件累计 usage；retry 插件只处理明确错误类。指标至少含 task state、policy violations、resource leaks、pass^k。

## 核心推导

插件职责正交可分别测试和替换。总分不应掩盖硬失败：先用 invariants gate，再报告连续指标。若任务 i 共跑 `n_i` 次且成功 `c_i` 次，论文的无偏经验估计为 `pass^k=(1/N)Σ_i C(c_i,k)/C(n_i,k)`，要求每个任务 `n_i≥k`；只有 `n_i=k` 时才退化为“该任务全部 k 次成功”的 0/1 指示量。

## 工业联系与事实标签

- [THEOREM] 任何硬不变量失败时令 acceptance=0，可保证高平均软分不能覆盖安全失败。
- [EMPIRICAL] τ-bench 的稳定性测量属于其重复运行协议。
- [INFERENCE] 评测 trace 应固定 seed/mock/version 并保留失败样本。
- [OPEN] 离线 proxy 与线上长期价值仍有分布偏差。

## 严格 60 分钟

- 0–5：核对固定 SHA；5–25：必读；25–35：运行 `practice.ts` 的组合数 pass^k 预检；35–55：在真实 capstone package 挂载 policy/audit/cost/retry 四个 Cordis 插件，运行多任务多 trial 定向 spec；55–60：保存 task-wise 报表、trace 与测试输出。

## 验收

预检覆盖完美、policy fail、`n<k`、`n>k`、`k=0` 与组合数经验估计；真实 checkout 的四插件 spec 证明各 checkpoint、卸载无残留，并提交 SHA、diff、命令、逐任务报表。不得用全局成功率、逐任务成功率的幂，或只适用于 `n=k` 的全成功指示量代替 `Σ_i C(c_i,k)/C(n_i,k)/N`。

## 可选延伸

加入 bootstrap confidence interval，不计时。
