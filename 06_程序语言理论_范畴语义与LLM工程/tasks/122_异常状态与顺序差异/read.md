# 第 122 晚：异常与状态的组合顺序

## 学习目标

- 比较 `StateT` over `Either` 与 `EitherT` over `State` 的可观察差异。
- 用反例说明 effect 组合通常不交换。

## 前置知识与关联任务

回顾 119 的 State/Maybe 与 121 的 effect 顺序。

## 必读材料（计入今晚 60 分钟）

| 分钟 | 材料 | 版本 | 精确范围 | 带着什么问题读 |
|---:|---|---|---|---|
| 11 | [Functional Programming in Lean](https://lean-lang.org/functional_programming_in_lean/monad-transformers.html) | official online book | 开头至 StateT/ExceptT 类型定义 | 两种 transformer 的结果类型括号怎样不同？ |
| 9 | 同书 | official | “Combining Monads”中的异常与状态示例 | 失败时已发生的状态更新可否观察？ |

## 精读导引

写出两种结果类型：`S→Either E (A,S)` 与 `S→(Either E A,S)`。前者失败时没有新状态，后者可以保留失败前状态。选择不是语法偏好，而是领域语义：事务需要回滚，审计计数可能必须保留。

## 必须完成的推导或证明

构造“先递增计数再失败”的计算，在两种堆叠中分别求值；说明哪一种满足回滚不变量。

## 代码实战

脚本实现两种最小 runner，比较相同动作序列的结果，并测试成功、立即失败和更新后失败。

## 与 DeepSeek Harness / LLM 工业应用的联系

工具失败时 durable `tool/call`、审计事件和实际外部写入是否保留，是必须明确的协议问题。Monad transformer 顺序提供最小反例生成器，不能代替 Harness 的显式补偿和 log 规则。

## 60 分钟安排

- 0–5：写两种嵌套类型。
- 5–25：精读 transformer 示例。
- 25–45：运行反例。
- 45–55：写回滚/审计两个需求的选择理由。
- 55–60：验收。

## 验收标准

- 能预测两种顺序的失败结果。
- 三类路径测试通过。
- 能把选择关联到一个明确业务不变量。

## 可选延伸

研究 distributive law of monads；不计入今晚。
