# 第 125 晚：Handler 的操作语义

## 学习目标

- 为 `return` 和每个 operation 写 handler 子句。
- 解释 deep handler 如何递归处理 continuation 后续产生的操作。

## 前置知识与关联任务

需要 124 的 free-effect AST 和 064–070 的小步/大步语义。

## 必读材料（计入今晚 60 分钟）

| 分钟 | 材料 | 版本 | 精确范围 | 带着什么问题读 |
|---:|---|---|---|---|
| 14 | [Pretnar tutorial](https://www.eff-lang.org/handlers-tutorial.pdf) | tutorial | §3，从 handler syntax 至 state handler 示例 | continuation 是恢复一次、零次还是多次？由谁决定？ |
| 6 | 同文 | tutorial | §4 的 operational semantics 开头和 handler reduction rules | handled operation 如何找到最近 handler？ |

## 精读导引

handler 是 computation 到另一 computation/值的解释器。return 子句处理纯结果，operation 子句获得参数与 continuation。调用 continuation 零次表示中止，多次可实现非确定性；有外部副作用时多次恢复尤其危险。deep handler 会继续处理恢复后的同类操作。

## 必须完成的推导或证明

逐步归约一个 `Get; Put; Get` 程序；标出 state handler 在何处把状态作为额外参数传递。

## 代码实战

为 124 的 AST 编写 state/log handler，比较同一程序的执行解释和纯 trace 解释；未知操作必须显式失败。

## 与 DeepSeek Harness / LLM 工业应用的联系

tools pre/execute/post 与 policy listener 是 handler-like 的工程结构；waterfall 的 `next()` 允许委托或短路。该对应是解释框架，不是形式等价声明。

## 60 分钟安排

- 0–5：写 return/operation 两类子句。
- 5–25：精读 handler 与归约规则。
- 25–46：实现两种解释器。
- 46–55：手推状态程序。
- 55–60：验收。

## 验收标准

- 正确解释 continuation 和 deep handling。
- 执行/trace 两个 handler 结果一致且未知操作失败。
- 能说明多次恢复外部工具的风险。

## 可选延伸

比较 shallow handler；不计入今晚。
