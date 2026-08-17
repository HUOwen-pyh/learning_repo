# 第 134 晚：Lexer 与 Token 契约

## 学习目标

- 将字符流确定性地切分为带位置的 token。
- 定义最长匹配、空白处理和非法字符的失败契约。

## 前置知识与关联任务

回顾 022–028 的语法/AST 和 027 的自动机。

## 必读材料（计入今晚 60 分钟）

| 分钟 | 材料 | 版本 | 精确范围 | 带着什么问题读 |
|---:|---|---|---|---|
| 12 | [LLVM Kaleidoscope Tutorial](https://llvm.org/docs/tutorial/MyFirstLanguageFrontend/LangImpl01.html) | LLVM current, checked 2026-08-15 | Chapter 1 “Lexer”从 token 枚举至 `gettok` 结束 | lexer 返回值如何区分字符、标识符、数字和 EOF？ |
| 8 | [Python lexical analysis reference](https://docs.python.org/3/reference/lexical_analysis.html) | Python 3.14 | §2.1 line structure 与 §2.3 identifiers 开头 | 位置信息和 Unicode 规则为何属于语言契约？ |

## 精读导引

先写 token 类型，再写扫描器。最长匹配意味着 `==` 不能被切成两个 `=`；错误 token 必须携带 offset，不能静默跳过。今天的 MiniPL 只接受 ASCII 标识符，明确这是课程子语言，不冒充 Python 规则。

## 必须完成的推导或证明

为 `let x=12+3` 写完整 token/跨度序列；构造 `12abc` 在两种语言规范下可能有的不同解释。

## 代码实战

实现带 span 的 lexer，覆盖 EOF、空白、关键字、整数、双字符运算符和非法字符。

## 与 DeepSeek Harness / LLM 工业应用的联系

流式 JSON/SSE/配置解析的第一层同样需要明确 token 边界和错误位置；错误恢复若吞字符会让后续 schema/策略检查失真。

## 60 分钟安排

- 0–5：列 token 类型。
- 5–25：精读 lexer 与词法契约。
- 25–47：运行并扩展 scanner。
- 47–55：写跨度序列与歧义例。
- 55–60：验收。

## 验收标准

- 每个 token 有半开 span。
- 最长匹配和非法字符测试通过。
- 能说明 lexer 与 parser 的责任边界。

## 可选延伸

处理 Unicode identifier；不计入今晚。
