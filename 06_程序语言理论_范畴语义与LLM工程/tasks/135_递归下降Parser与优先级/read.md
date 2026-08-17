# 第 135 晚：递归下降 Parser 与优先级

## 学习目标

- 把分层表达式文法直接翻译成递归下降函数。
- 用 AST 区分结合性与求值顺序。

## 前置知识与关联任务

需要 134 的 token 流和 022–028 的 BNF/AST。

## 必读材料（计入今晚 60 分钟）

| 分钟 | 材料 | 版本 | 精确范围 | 带着什么问题读 |
|---:|---|---|---|---|
| 14 | [LLVM Kaleidoscope Tutorial](https://llvm.org/docs/tutorial/MyFirstLanguageFrontend/LangImpl02.html) | LLVM current | Chapter 2 “Parser Basics”至 “Binary Expression Parsing”结束 | precedence climbing 如何决定何时结束右侧解析？ |
| 6 | [Software Foundations ImpParser](https://softwarefoundations.cis.upenn.edu/plf-current/ImpParser.html) | PLF current | “Lexical Analysis”后 parser combinator 的表达式层次部分 | 文法层级如何避免歧义？ |

## 精读导引

为每个优先级层写函数：atom→mul→add。左结合用循环累积，右结合通常递归。parser 应消费恰当 token 并在结尾确认 EOF；忽略尾随 token 会接受非法前缀。

## 必须完成的推导或证明

手画 `1+2*3+4` 的 AST，说明它为何不是 `((1+2)*3)+4`；再给 `^` 写右结合文法。

## 代码实战

实现整数、括号、`+`、`*` 的 parser/evaluator，加入缺右括号、尾随 token 和空输入反例。

## 与 DeepSeek Harness / LLM 工业应用的联系

配置表达式、schema 和约束生成器都依赖 parser 契约。结构化生成只有与 parser 接受语言完全一致，token mask 才安全。

## 60 分钟安排

- 0–5：写三层文法。
- 5–25：精读 parser。
- 25–47：运行并修改实现。
- 47–55：画 AST 与错误用例。
- 55–60：验收。

## 验收标准

- 优先级/结合性结果正确。
- 缺括号、尾随输入、空输入均拒绝。
- parser 消费位置可解释。

## 可选延伸

实现 Pratt parser；不计入今晚。
