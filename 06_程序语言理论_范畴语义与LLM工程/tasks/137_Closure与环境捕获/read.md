# 第 137 晚：Closure 与环境捕获

## 学习目标

- 将函数值表示为参数、函数体和定义时环境。
- 用反例证明只保存 AST 不足以实现词法作用域。

## 前置知识与关联任务

需要 102 的指数/闭包直觉和 136 的词法环境。

## 必读材料（计入今晚 60 分钟）

| 分钟 | 材料 | 版本 | 精确范围 | 带着什么问题读 |
|---:|---|---|---|---|
| 13 | [Cornell CS 3110 §10.4.3](https://cs3110.github.io/textbook/chapters/interp/environment.html) | online textbook，核验于 2026-08-15 | “A Second Attempt at Evaluating the Lambda Calculus in the Environment Model”全文：closure 构造与 application rules | `defenv` 在何时保存、在何时重新扩展？应用时为什么不能用调用点环境？ |
| 7 | [同章](https://cs3110.github.io/textbook/chapters/interp/environment.html) | 同版 | §10.4.4 实现说明与 §10.4.5 开头至 lambda-calculus fragment 的三条规则 | closure 怎样把代码和环境配成值？动态/词法开关会改变哪条规则？ |

## 精读导引

求值 lambda 时不执行函数体，而是冻结当前环境。应用时在捕获环境上扩展参数。若改用调用者环境，就变成动态作用域；若捕获整个可变字典的别名，还可能受到之后修改影响，需明确快照/共享语义。

## 必须完成的推导或证明

构造 `let x=1 in let f=λy.x+y in let x=100 in f 2`，分别给词法和动态作用域结果。

## 代码实战

扩展 MiniPL 为 `Lam/App`，实现 closure 快照；错误的动态 evaluator 必须在反例上给不同结果。

## 与 DeepSeek Harness / LLM 工业应用的联系

plugin/listener 捕获其 context 与 disposer owner。错误捕获 root context 或可变全局会造成越权、泄漏和卸载残留。

## 60 分钟安排

- 0–5：写 closure 三元组。
- 5–25：精读规则。
- 25–47：运行两种 evaluator。
- 47–55：完成作用域反例。
- 55–60：验收。

## 验收标准

- closure 使用定义时环境。
- 词法结果 3、动态结果 102 的反例可复现。
- 能解释快照与共享捕获的取舍。

## 可选延伸

研究 closure conversion；不计入今晚。
