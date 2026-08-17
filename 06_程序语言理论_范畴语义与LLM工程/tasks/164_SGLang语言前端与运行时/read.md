# 第164晚：SGLang 语言前端与运行时

## 目标与前置

- 目标：理解生成、选择、并行与外部函数如何成为 DSL 节点并由运行时调度。
- 前置：AST、解释器、异步任务概念。

## 计入 60 分钟的必读

| 分钟 | 材料 | 版本 | 精确范围 | 问题 |
|---:|---|---|---|---|
| 12 | [SGLang: Efficient Execution of Structured Language Model Programs](https://proceedings.neurips.cc/paper_files/paper/2024/file/724be4472168f31ba1c9ac630f15dec8-Paper-Conference.pdf) | NeurIPS 2024 | §2 Programming Model（PDF pp.3–4），含 Figure 2、language primitives 与 execution modes | 哪些控制结构属于语言前端？ |
| 8 | 同上 | 同版 | §3 RadixAttention 开头（PDF pp.4–5），只读 frontend hints 如何暴露共享前缀 | runtime 从程序中获得什么优化信息？ |

## 阅读导引

把 DSL 节点与模型 token 区分：Literal 本地追加，Generate 请求模型，Select 有候选集合，Fork 表示可并行分支。记录每种节点的输入输出状态。

## 核心推导

程序 AST 的小步解释为 ⟨node,state⟩→⟨node',state'⟩。显式结构使运行时看到共享前缀与并行边界；纯字符串 API 会丢失这些优化机会。

## 工业联系与事实标签

- [THEOREM] 对无循环的有限 AST，若每个原语终止，则结构递归解释器终止。
- [EMPIRICAL] SGLang 论文吞吐与延迟结果受模型、硬件、负载和基线配置限制。
- [INFERENCE] DSL IR 可同时承载观测、预算与策略元数据。
- [OPEN] 在隐藏后端差异的同时保留可移植性能仍需权衡。

## 严格 60 分钟

- 0–5：列节点；5–25：必读；25–48：运行解释器；48–55：增加 Select；55–60：解释 IR 的优化价值。

## 验收

顺序、分支、空程序断言通过；能指出哪些节点会触发模型。

## 可选延伸

阅读 §4 Efficient Constrained Decoding with Compressed Finite State Machine，不计时。
