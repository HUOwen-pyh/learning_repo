# 第 145 晚：CPS 变换与控制显式化

## 学习目标

- 将直接风格表达式转换为显式 continuation-passing style。
- 说明异常、早停和回调如何变成 continuation 选择。

## 前置知识与关联任务

需要 080 的 continuation、121 的计算 lambda calculus 和 138 的 CEK。

## 必读材料（计入今晚 60 分钟）

| 分钟 | 材料 | 版本 | 精确范围 | 带着什么问题读 |
|---:|---|---|---|---|
| 13 | [Cambridge Type Systems Lecture 10: Classical Logic and CPS](https://www.cl.cam.ac.uk/teaching/2425/Types/lec-10-handout.pdf) | 2024–25 | PDF pp.25–27，“Continuation-Passing Style (CPS) Translation”至 application 的 term translation | 原类型 `A` 经 CPS 后结果/continuation 类型怎样变化？application 规则为何先求函数？ |
| 7 | [同一讲义](https://www.cl.cam.ac.uk/teaching/2425/Types/lec-10-handout.pdf) | 2024–25 | PDF pp.28–29，“The CPS Translation for Continuations”与 `throw` preservation case | `letcont`/`throw` 怎样显式选择后续控制？类型保持证明依赖哪个归纳假设？ |

## 精读导引

CPS 函数不返回结果，而把结果交给 `k`。二元运算需要先给左子项 continuation，再给右子项 continuation。错误 continuation 可与成功 continuation 分离。变换会引入管理性 redex；正确性关注在最终 continuation 下观察一致。

## 必须完成的推导或证明

手工 CPS 转换 `(1+2)*3`，标出每个 continuation 参数；用恒等 continuation 化简出 9。

## 代码实战

实现算术 AST 的直接 evaluator 与 CPS evaluator，固定随机差分；加入 success/error 双 continuation 的除法。

## 与 DeepSeek Harness / LLM 工业应用的联系

Cordis waterfall listener 的 `next()` 是 around-middleware continuation：调用即委托，不调用即短路。CPS 能精确分析“谁拥有后续控制”。

## 60 分钟安排

- 0–5：写 CPS 函数类型。
- 5–25：精读 transform。
- 25–47：运行差分和错误 continuation。
- 47–55：手转表达式。
- 55–60：验收。

## 验收标准

- CPS/直接风格 100 个样例一致。
- 除零只进入 error continuation。
- 能解释 `next()` 的调用/短路语义。

## 可选延伸

做 defunctionalization 得抽象机；不计入今晚。
