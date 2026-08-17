# 第 126 晚：Free Effect 与处理器顺序综合

## 学习目标

- 构建含 State、Exception、ToolCall 的 free-effect 程序。
- 用可执行反例说明 handler 顺序会改变含义。

## 前置知识与关联任务

综合 120–125，特别是 122 的 effect 顺序和 125 的 continuation。

## 必读材料（计入今晚 60 分钟）

| 分钟 | 材料 | 版本 | 精确范围 | 带着什么问题读 |
|---:|---|---|---|---|
| 12 | [Pretnar tutorial](https://www.eff-lang.org/handlers-tutorial.pdf) | tutorial | §5 “Reasoning about handlers”中 handler equations 与示例 | 哪些程序等式依赖 handler 的具体解释？ |
| 8 | [Moggi, Notions of Computation and Monads](https://person.dibris.unige.it/moggi-eugenio/ftp/ic91.pdf) | Information and Computation 93(1), 1991 | PDF pp.2–4：Definitions 1.2–1.3 的 Kleisli 方程与 Lemma 1.4 的 monad 对应 | Monad 方程与某个具体 handler 方程有什么层次差异？ |

## 精读导引

自由语法只记录请求和 continuation；不同 handler 组合决定失败时回滚状态、工具是否真正执行、日志是否保留。先明确领域不变量，再选处理顺序。不要把一次通过测试的顺序推广为所有 effect 都交换。

## 必须完成的推导或证明

对“状态加一→工具调用→失败”列出 transactional 和 audit 两种语义，逐项比较状态、调用 trace 和返回值。

## 代码实战

完成两个 handler runner：事务型失败回滚，审计型失败保留 trace。断言相同 AST 的可观察结果不同但各自满足声明不变量。

## 与 DeepSeek Harness / LLM 工业应用的联系

模型工具执行必须明确 durable log、审批拒绝、外部副作用和错误的顺序。本晚是后续真实 tool pipeline 审计的理论小模型。

## 60 分钟安排

- 0–5：列出三类 effect。
- 5–25：精读 handler equations。
- 25–47：运行两个 runner。
- 47–55：写两套不变量和差异表。
- 55–60：阶段验收。

## 验收标准

- 同一 AST 可被至少两个 handler 解释。
- 回滚/审计断言和失败边界通过。
- 能用业务不变量论证顺序，而非凭偏好选择。

## 可选延伸

研究 effect rows 和 handler 类型推断；不计入今晚。
