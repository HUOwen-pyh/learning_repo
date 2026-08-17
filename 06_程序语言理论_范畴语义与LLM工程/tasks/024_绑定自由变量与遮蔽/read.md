# 第 024 晚：绑定、自由变量与遮蔽

## 学习目标

- 用作用域规则判定变量出现是自由还是受绑定。
- 实现自由变量集合与闭项判定。
- 解释同名内层绑定如何遮蔽外层绑定。

## 前置任务

- 第 022 晚“语法、BNF 与归纳 AST”。

## 必读材料（计入今晚 60 分钟）

| 分钟 | 材料 | 版本 | 精确范围 | 带着问题读 |
|---:|---|---|---|---|
| 15 | [PLFA — Lambda](https://plfa.github.io/22.08/Lambda/) | 22.08 | “Bound and free variables” 全节，至 closed/open examples 结束 | 一个名字能否在同一项的不同位置既自由又受绑定？ |
| 8 | [Software Foundations — Stlc](https://softwarefoundations.cis.upenn.edu/plf-current/Stlc.html) | PLF current，页面快照 2026-01 | “Syntax” 中 variables/abstractions/applications 与 scope 说明 | `λx. λx. x` 中最后的 `x` 指向谁？ |

## 精读导引

不要只给整项贴“自由/绑定”标签；标签属于变量的某次出现。沿 AST 路径维护当前绑定名字集合，并在进入 lambda 时扩展集合。再用集合递推式独立核对算法。

## 必须完成的推导

1. 推导 `FV(x)={x}`、`FV(t u)=FV(t)∪FV(u)`、`FV(λx.t)=FV(t)−{x}`。
2. 分别计算 `λx.x y` 与 `λx.(λx.x) x` 的自由变量。
3. 说明集合递推为什么自然处理遮蔽。

结论类型：【定义】闭项恰是自由变量集合为空的项。

## 与 DeepSeek Harness / LLM 工业应用的联系

这是基础层联系：prompt 模板变量、工具参数名和配置覆盖也有“声明—引用—遮蔽”问题。lambda 绑定提供一个小而精确的模型，帮助之后分析作用域泄漏与变量捕获。

## 60 分钟安排

| 环节 | 分钟 |
|---|---:|
| 必读材料 | 23 |
| 手算两项的自由变量 | 12 |
| 完成 `practice.py` | 20 |
| 运行验收 | 5 |
| **合计** | **60** |

## 验收标准

- 对变量的每个出现画出其最近 binder。
- 写出三条 `FV` 递推式。
- 代码通过闭项正例、开放项反例、双重遮蔽边界例。

## 可选延伸

- 实现 `occurrences(term)`，返回每个名字的自由/受绑定出现次数。

