# 第 039 晚：Progress 进展性

## 学习目标

- 精确陈述 progress 的 closed/well-typed 前提。
- 按 typing derivation 归纳处理应用 case。
- 实现返回 `done` 或 `step(next)` 的进展函数。

## 前置任务

- 第 038 晚“值与典范形式引理”。

## 必读材料（计入今晚 60 分钟）

| 分钟 | 材料 | 版本 | 精确范围 | 带着问题读 |
|---:|---|---|---|---|
| 19 | [PLFA — Properties](https://plfa.github.io/22.08/Properties/) | 22.08 | “Progress” 从两个 stuck counterexamples 至 application case 的逐项解释结束 | 应用 case 在何处使用 canonical form？ |
| 7 | [PLFA — Properties](https://plfa.github.io/22.08/Properties/) | 22.08 | Introduction 中 Progress/Preservation 两条陈述 | 为什么上下文必须为空？ |

## 精读导引

证明对“typing evidence”归纳，不对随意 AST 猜测。应用 case：函数子项先 progress；若 step 用 ξ₁，若 done 则典范形式给 lambda；再看实参，最终得到 ξ₂ 或 β。

## 必须完成的推导

1. 画出应用 case 的四叶决策树。
2. 给出 ill-typed stuck `true false`。
3. 给出 well-typed but open `f true`，说明空上下文条件不可删。

结论类型：【类型安全核心定理】若 `∅⊢t:T`，则 t 是值或存在 t′ 使 `t→t′`。

## 与 DeepSeek Harness / LLM 工业应用的联系

直接联系：静态验证通过的封闭工具请求应当“已完成”或存在合法下一动作，而不能卡在未定义协议状态。实际系统还需处理 I/O 错误；progress 不承诺外部服务成功。

## 60 分钟安排

| 环节 | 分钟 |
|---|---:|
| 必读材料 | 26 |
| 应用 case 决策树 | 13 |
| 完成 progress 程序 | 17 |
| 验收 | 4 |
| **合计** | **60** |

## 验收标准

- theorem 陈述不遗漏 empty context。
- typed non-value 必有下一步。
- β 正例、ill-typed 反例、lambda value 边界通过。

## 可选延伸

- 对深度 3 的闭项做枚举，自动搜索 progress counterexample。

