# 第 142 晚：AST 到栈机的代码生成

## 学习目标

- 递归编译表达式为栈指令，并保持语义。
- 写出编译器正确性的结构归纳命题。

## 前置知识与关联任务

需要 135/140 的 AST、139 的栈机和 141 的 verifier。

## 必读材料（计入今晚 60 分钟）

| 分钟 | 材料 | 版本 | 精确范围 | 带着什么问题读 |
|---:|---|---|---|---|
| 12 | [LLVM Kaleidoscope Ch.3](https://llvm.org/docs/tutorial/MyFirstLanguageFrontend/LangImpl03.html) | LLVM current | NumberExprAST 与 BinaryExprAST 的 codegen 实现 | 子表达式代码生成顺序怎样决定 operand 顺序？ |
| 8 | [Software Foundations PE](https://softwarefoundations.cis.upenn.edu/plf-current/PE.html) | PLF current | “Correctness of Constant Folding”前的 compiler/transform correctness 讨论 | 应证明结果相等还是 trace 相等？ |

## 精读导引

`compile(Add(a,b))=compile(a)++compile(b)++[ADD]`。正确性命题最好参数化初始栈：执行编译代码得到 `eval(term)::stack`。这样归纳步骤可直接使用两个子项假设。

## 必须完成的推导或证明

对 AST 做结构归纳，证明上述参数化命题；明确使用指令序列拼接的结合律。

## 代码实战

实现编译器、VM 和固定随机 differential test；再把错误的子表达式顺序用于减法，捕获非交换反例。

## 与 DeepSeek Harness / LLM 工业应用的联系

prompt/工具 schema/Remote 类型生成同样是程序变换。每个生成器都应有可执行 oracle 或保持性质，而不是只比 snapshot 文本。

## 60 分钟安排

- 0–5：写编译方程。
- 5–25：精读 codegen/正确性。
- 25–47：运行差分测试。
- 47–55：完成归纳和减法反例。
- 55–60：验收。

## 验收标准

- 100 个随机 AST 与解释器一致。
- verifier 接受所有生成代码。
- 归纳命题包含任意初始栈。

## 可选延伸

加入变量槽；不计入今晚。
