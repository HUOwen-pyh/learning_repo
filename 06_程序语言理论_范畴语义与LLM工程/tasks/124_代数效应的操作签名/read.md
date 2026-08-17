# 第 124 晚：代数效应的操作签名

## 学习目标

- 用操作名、参数类型和结果类型描述 effect signature。
- 把程序分成纯返回、操作请求和 continuation。

## 前置知识与关联任务

需要 010 的代数签名、120 的值/计算 AST 和 117 的 continuation 组合。

## 必读材料（计入今晚 60 分钟）

| 分钟 | 材料 | 版本 | 精确范围 | 带着什么问题读 |
|---:|---|---|---|---|
| 13 | [Pretnar, An Introduction to Algebraic Effects and Handlers](https://www.eff-lang.org/handlers-tutorial.pdf) | tutorial | §1 “Computational effects”与 §2 中 operations 定义 | operation 的返回值为何交给 continuation？ |
| 7 | 同文 | tutorial | §2 的 state/read-write 示例 | effect signature 与具体 handler 如何解耦？ |

## 精读导引

操作 `get:Unit→State`、`put:State→Unit` 只是语法/接口；handler 决定它们如何解释。Free-effect 树把 continuation 显式保留，因此可以由不同 handler 解释为真实执行、模拟、日志或拒绝。不要把操作请求本身误认为 effect 已发生。

## 必须完成的推导或证明

给 ToolCall 写签名 `Call:Request→Response`，展开“调用后按响应分支”的 free-effect 节点类型。

## 代码实战

构造 `Pure`/`Op` free-effect AST，实现 `bind`；生成一棵包含 Ask 和 Log 的程序树，并检查结构而不执行操作。

## 与 DeepSeek Harness / LLM 工业应用的联系

模型生成 tool call，工具流水线再做 schema、策略、批准和执行。把“请求”与“解释”分离正是可测试、可替换 agent harness 的关键价值。

## 60 分钟安排

- 0–5：写三个操作签名。
- 5–25：精读 operation/free computation。
- 25–46：构建并绑定 AST。
- 46–55：完成 ToolCall 类型展开。
- 55–60：验收。

## 验收标准

- 区分 signature、request 和 handler。
- AST bind 保持 continuation 且断言通过。
- 能画出一次 tool call 的操作树。

## 可选延伸

阅读 free monad 与 algebraic theory 的关系；不计入今晚。
