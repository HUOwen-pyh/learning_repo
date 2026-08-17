# 第 146 晚：常量折叠与语义保持

## 学习目标

- 定义优化的语义保持命题并用结构归纳证明。
- 用 overflow、异常和 effect 反例限制不安全折叠。

## 前置知识与关联任务

需要 140 的 evaluator、142 的编译正确性和 104 的语义等式。

## 必读材料（计入今晚 60 分钟）

| 分钟 | 材料 | 版本 | 精确范围 | 带着什么问题读 |
|---:|---|---|---|---|
| 15 | [Software Foundations PE](https://softwarefoundations.cis.upenn.edu/plf-current/PE.html) | PLF current | “Constant Folding”与 “Correctness of Constant Folding”证明 | 归纳假设在哪些 AST 构造子上使用？ |
| 5 | 同章 | PLF current | soundness theorem 陈述 | 行为相等的量化对象是什么？ |

## 精读导引

纯整数加法可在两个常量子项时折叠。若语言有溢出、除零、日志或随机数，宿主 Python 的运算语义可能与目标语言不同；必须用目标语义求折叠值。`eval(opt(t))=eval(t)` 对所有环境成立才是所需命题。

## 必须完成的推导或证明

对 Add 构造分“两个优化后子项均常量”和其余情况证明保持；指出 effectful Print 节点为何不可删。

## 代码实战

实现含 `Print(value, body)` 的值/trace 语义、保持 Print 的正确常量折叠和固定随机 differential test；坏优化器用 `x*0→0` 删除 effectful 子项，反例必须得到相同值但不同 trace。

## 与 DeepSeek Harness / LLM 工业应用的联系

prompt/schema/config 归一化若改变顺序或删除注册，可能破坏可观察 effect。优化必须声明观察模型：值、错误、事件、延迟或资源。

## 60 分钟安排

- 0–5：写保持命题。
- 5–25：精读实现和证明。
- 25–47：运行差分与 trace 反例。
- 47–55：完成 Add 归纳。
- 55–60：验收。

## 验收标准

- 纯 AST 200 个差分通过。
- effect trace 反例能击穿坏优化。
- 证明明确量化环境和观察。

## 可选延伸

研究 dead-code elimination；不计入今晚。
