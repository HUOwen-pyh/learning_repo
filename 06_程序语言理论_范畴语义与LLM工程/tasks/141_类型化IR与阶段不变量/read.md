# 第 141 晚：类型化 IR 与阶段不变量

## 学习目标

- 定义源 AST 到中间表示的显式类型/栈效应契约。
- 将编译阶段不变量与用户语言类型规则分开。

## 前置知识与关联任务

需要 036–060 的类型检查、140 的解释器与 139 的字节码机。

## 必读材料（计入今晚 60 分钟）

| 分钟 | 材料 | 版本 | 精确范围 | 带着什么问题读 |
|---:|---|---|---|---|
| 12 | [LLVM Kaleidoscope Ch.3](https://llvm.org/docs/tutorial/MyFirstLanguageFrontend/LangImpl03.html) | LLVM current | “Code Generation Setup”至 expression codegen 方法 | 每个 AST 节点 codegen 的成功/失败契约是什么？ |
| 8 | [Cornell CS 4120 Type Systems notes](https://www.cs.cornell.edu/courses/cs4120/2026sp/notes.html?id=typesystems) | Spring 2026 | typing judgment 与 compiler guarantees 段 | 静态类型信息怎样成为后续阶段假设？ |

## 精读导引

IR 可以比源语言更显式：变量槽、基本块、指令结果类型和控制边。编译前先类型检查，编译后再验证 IR；不能让 codegen 的 `None` 静默代表任意错误。今天用 stack-effect `(pop,push)` 作为最小类型系统。

## 必须完成的推导或证明

为 `CONST`、`ADD`、`DUP` 写栈类型迁移，证明良类型指令序列运行时不 underflow。

## 代码实战

实现字节码 verifier，计算每个程序点的 stack height；拒绝 underflow 和终态高度不为 1。

## 与 DeepSeek Harness / LLM 工业应用的联系

Harness 的 Host/Client build、Typert 生成契约和 runtime schema 同样形成多阶段不变量。生成成功不等于运行时契约自动正确，需各阶段验证。

## 60 分钟安排

- 0–5：写 source/IR 两层契约。
- 5–25：精读 codegen/type guarantees。
- 25–46：运行 verifier。
- 46–55：证明无 underflow。
- 55–60：验收。

## 验收标准

- 正确程序每点高度确定。
- underflow/多余结果被拒绝。
- 能解释源类型与 IR verifier 的不同职责。

## 可选延伸

为栈中每项加入具体类型；不计入今晚。
