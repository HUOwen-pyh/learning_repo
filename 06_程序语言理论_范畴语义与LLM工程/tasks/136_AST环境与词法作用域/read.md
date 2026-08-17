# 第 136 晚：AST、环境与词法作用域

## 学习目标

- 用环境映射解释变量、let 与遮蔽。
- 区分词法作用域和动态作用域的查找时刻。

## 前置知识与关联任务

需要 135 的 AST、022–028 的绑定和 061–070 的环境语义。

## 必读材料（计入今晚 60 分钟）

| 分钟 | 材料 | 版本 | 精确范围 | 带着什么问题读 |
|---:|---|---|---|---|
| 12 | [Cornell CS 3110 §10.4 Environment Model](https://cs3110.github.io/textbook/chapters/interp/environment.html) | online textbook，核验于 2026-08-15 | §10.4 开头至 §10.4.1 的 variable、function、application、`let` big-step rules | 环境扩展后旧绑定如何保留并被遮蔽？环境模型相对 substitution 延迟了什么工作？ |
| 8 | [同章](https://cs3110.github.io/textbook/chapters/interp/environment.html) | 同版 | §10.4.2 “Lexical vs. Dynamic Scope”，读完 name-irrelevance 与 exception 类比 | 定义点环境和调用点环境分别产生什么结果？为什么一致改名不应改变含义？ |

## 精读导引

环境是不变映射的链式扩展，不要在退出 let 后遗留局部绑定。变量查找失败应显式报错。环境保存值，store 保存位置到值；今天没有可变引用，先不混用两者。

## 必须完成的推导或证明

推导 `let x=1 in (let x=2 in x)+x`，明确每个 `x` 绑定；构造动态作用域会给不同结果的函数例。

## 代码实战

实现 `Num/Var/Add/Let` 环境解释器，验证遮蔽、作用域退出和未绑定变量。

## 与 DeepSeek Harness / LLM 工业应用的联系

Cordis plugin context 类似分层能力环境；agent-scoped context 可遮蔽/增加注册。类比只帮助理解查找，真实生命周期还受 effect/fiber 管理。

## 60 分钟安排

- 0–5：画环境链。
- 5–25：精读环境规则。
- 25–46：运行解释器。
- 46–55：推导遮蔽例和动态反例。
- 55–60：验收。

## 验收标准

- let 退出后外层环境未被修改。
- 遮蔽/未绑定/边界测试通过。
- 能区分 environment 与 store。

## 可选延伸

实现 de Bruijn 环境；不计入今晚。
