# 第 060 晚：依赖类型：索引携带不变量

## 具体目标

- 理解值索引类型和 dependent function 的信息流。
- 用 Python 的受检构造器模拟 `Fin n`、`Vec A n`。
- 把 append 的长度方程写成可执行不变量。

## 前置编号

- 必须完成：053、057
- 闭卷入口问题：普通 `List A` 与 `Vec A n` 的类型信息差在哪里？

## 必读（20 分钟，已计入 60 分钟）

| 分钟 | 开放权威一手材料与版本 | 精确章节、页码或页内标题 | 阅读问题 |
|---:|---|---|---|
| 5–15 | [Cambridge Topics in Type Systems 2024–25](https://www.cl.cam.ac.uk/teaching/2425/Types/materials.html) | Lecture 11 “Introduction to dependent types” 与 Lecture 12 “Dependent type theory”，indexed families/Pi types 部分 | 为什么 `lookup : Fin n → Vec A n → A` 不需要运行时越界分支？ |
| 15–25 | [PLFA，Quantifiers](https://plfa.inf.ed.ac.uk/Quantifiers/) | 页内标题 “Universals”, “Existentials” 与依赖函数表示部分 | 依赖函数类型与普通全称量词如何对应？ |

只读指定边界；链接均为大学官方讲义、作者版本或正式论文页面。

## 导读

Python 不能静态证明依赖类型，但可以把同一不变量放入构造器和测试，观察真正依赖类型会把哪些运行时检查提前。关键不是把 `length` 字段称作证明，而是区分模拟与类型级保证。

## 必做推导 / 证明

写 `append : Vec A m → Vec A n → Vec A (m+n)` 的类型；对空向量和 cons 分支分别说明索引如何化简。

必须保留判断形式和规则名；“凭直觉显然”不算完成。

## DeepSeek Harness / LLM 工程联系

工具 schema 常有跨字段约束，如参数数量必须与占位符数量一致。依赖类型展示了如何让这类关系成为接口的一部分，而不仅是自然语言说明。

这是从形式概念到工程约束的映射；除明确指出外，不宣称 Harness 已静态证明这些性质。

## 严格 60 分钟

| 时间 | 工作 |
|---:|---|
| 0–5 | 回忆入口问题，写定义和反例 |
| 5–25 | 完成必读表并回答两个问题 |
| 25–38 | 手写推导或证明 |
| 38–55 | 运行 `practice.py`，再完成文件顶部的动手改造 |
| 55–60 | 按验收项自测并记录一个疑问 |

5 + 20 + 13 + 17 + 5 = 60 分钟。下面的延伸不得挤入本晚。

## 验收

- [ ] 能解释 `Fin n` 排除越界索引的机制。
- [ ] 脚本覆盖合法 lookup、越界、空向量和 append 长度。
- [ ] 动手改造：实现保持长度的 `map`。

## 可选延伸（不计时）

用 Lean/Agda 真正声明 `Vec` 和 `lookup`，比较 Python 模拟缺失了什么。

