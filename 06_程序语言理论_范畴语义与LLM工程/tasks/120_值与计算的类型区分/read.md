# 第 120 晚：值与计算的类型区分

## 学习目标

- 区分值类型 `A` 与产生 `A` 的计算类型 `T A`。
- 解释 call-by-value 的计算 lambda calculus 为什么显式引入 `T`。

## 前置知识与关联任务

回顾 116–119 的 Monad，以及 029–035 的求值策略。

## 必读材料（计入今晚 60 分钟）

| 分钟 | 材料 | 版本 | 精确范围 | 带着什么问题读 |
|---:|---|---|---|---|
| 16 | [Moggi, Notions of Computation and Monads](https://person.dibris.unige.it/moggi-eugenio/ftp/ic91.pdf) | Information and Computation 93(1), 1991 | PDF pp.1–3：Introduction 第 1–4 点、§1 开头、Example 1.1 与 Definition 1.2 | 为什么语义不能把有 effect 的程序仍解释为普通 `A→B`？`A` 与 `TA` 各表示什么？ |
| 4 | [Functional Programming in Lean: Monads](https://lean-lang.org/functional_programming_in_lean/monads.html) | official online book | “The Monad Type Class”定义框 | `pure`、`bind` 如何连接值与计算？ |

## 精读导引

把纯函数 `A→B` 与 effectful 函数 `A→T B` 并排写。`T` 不是“装盒子的语法技巧”，而是语义中对计算行为的抽象；不同 `T` 可表示部分性、异常、状态或非确定性。今天只建立类型边界，不把所有真实 I/O 都宣称已由一个简单 Monad 完整建模。

## 必须完成的推导或证明

给解析失败和状态读写各写一条 Kleisli 类型；说明若擦除 `T`，哪些失败/状态信息会在类型中消失。

## 代码实战

实现 `Return/Fail/Get/Put` 的计算 AST，静态区分值节点和计算节点；错误地把 `Fail` 当普通整数的程序必须被拒绝。

## 与 DeepSeek Harness / LLM 工业应用的联系

LLM adapter、工具和文件操作都可能失败、取消或产生事件。显式区分值与计算能防止调用者漏掉协议分支；Harness 最终用 TypeScript unions、事件和运行时 schema 实现这些边界。

## 60 分钟安排

- 0–5：写 `A→B` 与 `A→TB`。
- 5–25：精读 Moggi 与接口定义。
- 25–46：运行计算 AST 检查器。
- 46–55：完成两个类型推导和坏例。
- 55–60：验收。

## 验收标准

- 能解释 `A`/`TA` 的语义区别。
- 正确/错误 AST 被检查器区分。
- 不把 Monad 与任意“容器”同义化。

## 可选延伸

阅读 Moggi §2 余下演算；不计入今晚。
