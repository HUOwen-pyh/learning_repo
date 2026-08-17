# 第 123 晚：Functor、Applicative 与 Monad Transformer

## 学习目标

- 区分 `map`、独立 effect 的 applicative 组合和依赖前值的 monadic bind。
- 解释 transformer 为何需要提升底层计算。

## 前置知识与关联任务

需要 106 的函子、119 的 Monad 和 122 的堆叠顺序。

## 必读材料（计入今晚 60 分钟）

| 分钟 | 材料 | 版本 | 精确范围 | 带着什么问题读 |
|---:|---|---|---|---|
| 10 | [Functional Programming in Lean](https://lean-lang.org/functional_programming_in_lean/functor-applicative-monad.html) | official | Functor、Applicative、Monad 三个接口定义及关系 | 哪个接口允许第二步结构依赖第一步的值？ |
| 10 | [Monad Transformers](https://lean-lang.org/functional_programming_in_lean/monad-transformers.html) | official | transformer 与 `MonadLift` 的定义段 | `lift` 保留底层计算的哪些行为？ |

## 精读导引

`map` 只改变纯结果；Applicative 组合已知形状的独立计算；Monad 允许后续计算由前值决定。接口越强，可做的重排越少。Transformer 将一个 effect 参数化在底层 Monad 上，`lift` 嵌入底层动作，但不会自动解决不同 effect 的交换问题。

## 必须完成的推导或证明

给两个独立校验写 applicative 组合，再构造一个第二次查询依赖第一次返回 ID 的例子，说明为何必须 bind。

## 代码实战

实现 Validation applicative，累积多个错误；与 Either bind 的首错短路比较。再实现最小 `ExceptT` over `State`、`bind` 和 `lift`，验证被提升的底层状态动作保留状态变化，而异常会短路后续动作。

## 与 DeepSeek Harness / LLM 工业应用的联系

配置/schema 校验适合累积独立错误，工具执行则常需短路并依赖前一步结果。选对抽象能直接改善诊断和并发机会。

## 60 分钟安排

- 0–5：写三个接口的核心类型。
- 5–25：精读接口与 lift。
- 25–45：运行 Validation/Either 对照。
- 45–55：完成独立/依赖例子。
- 55–60：验收。

## 验收标准

- 能按依赖结构选择 Applicative 或 Monad。
- 错误累积和短路测试通过。
- `bool` 不被误收为年龄，且 `lift`/transformer 测试通过。
- 不声称 transformer 顺序无关。

## 可选延伸

研究 selective applicative functors；不计入今晚。
