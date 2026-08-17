# 第 140 晚：MiniPL 解释器综合

## 学习目标

- 串联 lexer、parser、AST、closure 与求值器。
- 用 differential oracle 和错误 span 验收完整前端。

## 前置知识与关联任务

综合 134–139；回顾 029 的属性测试和 064–070 的语义 trace。

## 必读材料（计入今晚 60 分钟）

| 分钟 | 材料 | 版本 | 精确范围 | 带着什么问题读 |
|---:|---|---|---|---|
| 10 | [LLVM Kaleidoscope Ch.1](https://llvm.org/docs/tutorial/MyFirstLanguageFrontend/LangImpl01.html) 与 [Ch.2](https://llvm.org/docs/tutorial/MyFirstLanguageFrontend/LangImpl02.html) | LLVM current | 回看 lexer/parser/AST 三个接口边界 | 每层应接受和返回什么，错误由谁拥有？ |
| 10 | [Software Foundations ImpParser](https://softwarefoundations.cis.upenn.edu/plf-current/ImpParser.html) | PLF current | “Putting It All Together”及 parser correctness discussion | round-trip/语义一致性可怎样分层测试？ |

## 精读导引

综合项目不再增加语法；重点是层间契约。`parse(lex(src))` 只构造 AST，evaluator 不应再读取源码文本。错误必须停在最早知道责任的层。随机生成小 AST，pretty-print 后解析，与直接 AST 求值比较。

## 必须完成的推导或证明

写出 `eval(parse(print(ast)))=eval(ast)` 的适用前提；给非单射 pretty-printer 一个不影响语义但影响结构 round-trip 的例子。

## 代码实战

脚本串联自有 lexer、递归下降 parser、AST、pretty-printer 与词法 closure evaluator；固定随机 AST 检查 `parse(pretty(t))=t` 及求值差分，并让非法 token 报出位置。

## 与 DeepSeek Harness / LLM 工业应用的联系

真实 agent 系统同样由协议解析、类型/schema、状态转换和 effect 执行分层组成。层间可重放契约比端到端一次成功更能定位错误。

## 60 分钟安排

- 0–5：画四层接口。
- 5–25：精读整合与正确性讨论。
- 25–48：运行差分/round-trip 测试。
- 48–55：写性质前提和反例。
- 55–60：阶段验收。

## 验收标准

- 100 个固定随机 AST 差分通过。
- 非法语法在 parser 层失败。
- 能说明结构相等与语义相等的区别。

## 可选延伸

加入 source map；不计入今晚。
