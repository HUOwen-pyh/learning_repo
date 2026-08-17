# 第 147 晚：编译器差分与阶段综合

## 学习目标

- 建立 `source→AST→optimized AST→IR→VM` 的分阶段 oracle。
- 在失败时缩小到最早发生分歧的阶段。

## 前置知识与关联任务

综合 141–146 和 029 的属性测试；需要能运行解释器与 VM 两套独立语义。

## 必读材料（计入今晚 60 分钟）

| 分钟 | 材料 | 版本 | 精确范围 | 带着什么问题读 |
|---:|---|---|---|---|
| 10 | [LLVM Kaleidoscope Tutorial overview](https://llvm.org/docs/tutorial/MyFirstLanguageFrontend/index.html) | LLVM current | Ch.1–5 目录与各章产物摘要 | 每个阶段的输入、输出和独立检查是什么？ |
| 10 | [Software Foundations PE](https://softwarefoundations.cis.upenn.edu/plf-current/PE.html) | PLF current | “Correctness of Constant Folding”及测试讨论复读 | 测试与证明各覆盖哪类失败？ |

## 精读导引

不要只比较源码与最终输出。先检查 parse/pretty round-trip，再比较 AST 与优化 AST 语义，再验证 IR，最后比较 VM。保存 seed、最小 AST、各阶段中间表示。Differential test 的两个实现若共享同一个 bug 就会同时错，因此关键层应再有小规模数学 oracle。

## 必须完成的推导或证明

写出四段保持关系如何传递得到端到端保持；指出任一关系只有测试证据时，最终结论的证据等级。

## 代码实战

脚本对 300 个固定随机表达式跑解释、优化、编译、验证、VM；故障注入后用递归 shrink 找更小反例。

## 与 DeepSeek Harness / LLM 工业应用的联系

Harness 有生成类型、序列化、stream 翻译、event projection 和 replay 等多阶段边界。阶段化 oracle 比一次 e2e snapshot 更能定位工业故障。

## 60 分钟安排

- 0–5：画 pipeline。
- 5–25：精读阶段与正确性。
- 25–49：运行 300 例及故障注入。
- 49–55：写保持关系链。
- 55–60：阶段验收。

## 验收标准

- 300 个样例通过所有阶段断言。
- 故障注入产生可复现、缩小后的反例。
- 能标注每段结论是 THEOREM、TESTED 还是 INFERENCE。

## 可选延伸

引入翻译验证；不计入今晚。
