# 第 046 晚：位置、store 与带状态的小步语义

## 学习目标

- 区分 source-level reference 与 runtime location。
- 将一步关系从 `t→t′` 扩为 `(t,μ)→(t′,μ′)`。
- 实现分配、解引用、赋值的纯配置变换。

## 前置任务

- 第 041–042 晚 preservation 与安全 runner。

## 必读材料（计入今晚 60 分钟）

| 分钟 | 材料 | 版本 | 精确范围 | 带着问题读 |
|---:|---|---|---|---|
| 12 | [Software Foundations — References](https://softwarefoundations.cis.upenn.edu/plf-current/References.html) | PLF current，页面快照 2026-01 | “Operational Semantics” → “Locations” 与 “Stores” | location 为什么只应在中间运行项出现？ |
| 15 | [Software Foundations — References](https://softwarefoundations.cis.upenn.edu/plf-current/References.html) | PLF current，页面快照 2026-01 | “Reduction” 的 ST_RefValue、ST_DerefLoc、ST_Assign 及关系形状说明 | 哪些规则改变 store，哪些只读/传播它？ |

## 精读导引

把配置作为不可分的 `(term, store)`。`ref v` 在尾部新增 cell 并返回新 location；`!loc` 读取不改 store；`loc:=v` 替换 cell 并返回 Unit。不要把 location 当用户可猜的普通整数。

## 必须完成的推导

1. `(ref true,[])→(loc 0,[true])`。
2. `(!loc 0,[true])→(true,[true])`。
3. `(loc 0:=false,[true])→(unit,[false])`。

结论类型：【状态语义】副作用通过配置转移显式表示；term-only relation 已不足以描述计算。

## 与 DeepSeek Harness / LLM 工业应用的联系

直接联系：agent action 不只生成下一条消息，还改变环境/工具状态。可回放 Harness 必须把 action 前后 state 一并记录；仅保存文本轨迹无法重建副作用。

## 60 分钟安排

| 环节 | 分钟 |
|---|---:|
| 必读材料 | 27 |
| 三条配置转移推导 | 11 |
| 完成 store 机器 | 18 |
| 验收 | 4 |
| **合计** | **60** |

## 验收标准

- 分配返回 fresh location。
- 读不修改 store，写产生新 store 配置。
- 分配正例、越界反例、loc0 边界通过。

## 可选延伸

- 加 `Seq`，运行 allocate→assign→deref 的完整轨迹。

