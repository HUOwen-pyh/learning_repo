# 第 119 晚：Maybe、List、State Monad 定律综合

## 学习目标

- 在 `map/pure/bind` 表示下验证三条 Monad 定律。
- 识别“能运行的封装类型”不一定是合法 Monad。

## 前置知识与关联任务

综合 113–118；必须能在 `η/μ` 与 `pure/bind` 两种表示间转换。

## 必读材料（计入今晚 60 分钟）

| 分钟 | 材料 | 版本 | 精确范围 | 带着什么问题读 |
|---:|---|---|---|---|
| 12 | [Functional Programming in Lean](https://lean-lang.org/functional_programming_in_lean/monads.html) | official online book | “The Monad Type Class”至首个 law discussion | `pure` 与 `bind` 的类型怎样限制实现？ |
| 8 | [Riehl, Category Theory in Context](https://emilyriehl.github.io/files/context.pdf) | author PDF | §5.1 Monad laws 图表复读 | 代码三律怎样对应自然变换图表？ |

## 精读导引

对函数 `f:A→M B`、`g:B→M C`，左右单位和结合律必须对所有值成立。State 的相等是运行在所有初始状态后的外延相等，不能比较 Python 函数对象身份。测试可以找到反例，普遍正确仍需参数化推理。

## 必须完成的推导或证明

分别给 Maybe、List、State 写一个结合律等式；说明 State 为什么要量化初态。

## 代码实战

统一 law runner 检查三种 Monad，并让一个会重复调用 continuation 的坏 State bind 失败。

## 与 DeepSeek Harness / LLM 工业应用的联系

LLM 工具链常组合失败、列表候选和状态更新。定律让重构括号不改变含义；但异步取消、外部 I/O 和可撤销注册需要更细的 effect 模型。

## 60 分钟安排

- 0–5：闭卷写三律。
- 5–25：精读代码与图表表示。
- 25–47：运行统一 law tests。
- 47–55：分析坏 State bind。
- 55–60：阶段验收。

## 验收标准

- 三种 Monad 的左右单位与结合律通过。
- State 采用外延测试而非函数身份。
- 能构造并解释一个违反定律的实现。

## 可选延伸

证明 continuation Monad 定律；不计入今晚。
