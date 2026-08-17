# 第159晚：Inspect 任务与 Solver

## 目标与前置

- 目标：把 dataset、solver、scorer 组织成可重复评测任务。
- 前置：纯函数、数据类、测试夹具。

## 计入 60 分钟的必读

| 分钟 | 材料 | 版本 | 精确范围 | 问题 |
|---:|---|---|---|---|
| 12 | [Inspect Tasks](https://inspect.aisi.org.uk/tasks.html) | checked_at 2026-08-15 | Task Basics：Task、Dataset、Solver、Scorer | 一个 task 最少固定哪些对象？ |
| 8 | 同上 | 同页 | Solvers：generate 与 chain | solver 的中间状态如何传递？ |

## 阅读导引

把样本数据、推理过程、评分规则分离。阅读代码示例时记录哪些参数属于实验配置，哪些属于每个 sample 的动态状态。

## 核心推导

评测可写成 map(score ∘ solve, dataset)，但真实 solver 可能有状态或并发副作用。因此需要 sample id、固定配置和逐样本 trace，才能定位非确定性来源。

## 工业联系与事实标签

- [THEOREM] 对有限 dataset 和终止的纯 solver/scorer，顺序 map 必然产生与样本数相同的结果。
- [EMPIRICAL] Inspect 文档展示当前框架 API；依赖版本升级时应锁定环境。
- [INFERENCE] 将 scorer 独立于 agent 可防止业务规则被提示改写。
- [OPEN] 单一离线数据集对真实工具分布漂移的代表性有限。

## 严格 60 分钟

- 0–5：定义 sample；5–25：必读；25–48：运行 task pipeline；48–55：加入 solver chain；55–60：检查 trace。

## 验收

全对、全错、空 dataset 均通过；结果保留 sample id。

## 可选延伸

阅读 Inspect sandboxing 文档，不计时。
