# 第 036 晚：STLC 类型、上下文与判断规则

## 学习目标

- 写出 Bool 与箭头类型的语法。
- 阅读判断 `Γ ⊢ t : T` 的输入、输出与假设。
- 为变量、抽象、应用构造显式推导树。

## 前置任务

- 第 011 晚“归纳关系与推导树”。
- 第 029–035 晚“无类型 lambda”。

## 必读材料（计入今晚 60 分钟）

| 分钟 | 材料 | 版本 | 精确范围 | 带着问题读 |
|---:|---|---|---|---|
| 15 | [Software Foundations — Stlc](https://softwarefoundations.cis.upenn.edu/plf-current/Stlc.html) | PLF current，页面快照 2026-01 | “Overview”；“Syntax” 中 Types/Terms | 类型注解放在哪里，消除了哪种搜索？ |
| 11 | [Software Foundations — Stlc](https://softwarefoundations.cis.upenn.edu/plf-current/Stlc.html) | PLF current，页面快照 2026-01 | “Typing” 从 contexts 到 T_Var/T_Abs/T_App/T_True/T_False/T_If | 每条规则的 premise 如何缩小为子项？ |

## 精读导引

把 `Γ` 当有限映射，不当运行时环境。对 `λx:Bool.x` 从叶子 T_Var 向上画 T_Abs；对应用先推出函数是箭头类型，再要求实参类型与定义域精确相同。

## 必须完成的推导

1. 推导 `∅ ⊢ λx:Bool.x : Bool→Bool`。
2. 推导 `∅ ⊢ (λx:Bool.x) true : Bool`。
3. 证明 `true false` 无法由 T_App 收尾。

结论类型：【定义】typing judgment 是由规则生成的关系；推导对象记录其证据。

## 与 DeepSeek Harness / LLM 工业应用的联系

这是基础且直接的契约模型：上下文对应可用工具/变量的静态接口，推导树对应验证理由。Harness 可用类似结构在执行前拒绝工具名或参数类型不匹配的轨迹。

## 60 分钟安排

| 环节 | 分钟 |
|---|---:|
| 必读材料 | 26 |
| 三棵推导树 | 13 |
| 完成推导器 | 17 |
| 验收 | 4 |
| **合计** | **60** |

## 验收标准

- 能逐 premise 解释 T_Var/T_Abs/T_App。
- 输出对象保留 rule、结论和子推导。
- identity 正例、错应用反例、遮蔽边界例通过。

## 可选延伸

- 把推导树 pretty-print 为横线式自然演绎格式。

