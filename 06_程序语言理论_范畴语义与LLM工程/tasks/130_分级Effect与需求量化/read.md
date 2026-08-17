# 第 130 晚：分级 Effect 与需求量化

## 学习目标

- 用幺半群 grade 描述计算的 effect/资源上界。
- 区分普通 effect set、计数 grade 与顺序 trace。

## 前置知识与关联任务

回顾 015–021 的幺半群、124–126 的 effect signature 和 128 的需求代数。

## 必读材料（计入今晚 60 分钟）

| 分钟 | 材料 | 版本 | 精确范围 | 带着什么问题读 |
|---:|---|---|---|---|
| 13 | [Orchard, Wadler & Eades, Unifying graded and parameterised monads](https://arxiv.org/abs/2001.10274) | author preprint | §1 与 §2 中 graded monad 的类型和动机 | bind 时 grade 为什么按幺半运算合并？ |
| 7 | [Coeffects](https://tomasp.net/academic/papers/coeffects/) | ICALP 2014 | §4 语法性质概览 | grade 是精确值还是上界，取决于什么判断？ |

## 精读导引

给 `T_m A` 的索引 `m` 一个明确代数。effect 集用并集、调用次数用加法、顺序 trace 用拼接；它们表达的信息不同。若策略关心“先审批再执行”，集合 grade 会丢失顺序，必须升级到 trace/自动机。

## 必须完成的推导或证明

为两个工具动作的 bind 分别计算集合、次数和 trace grade；构造集合相同但顺序违规的反例。

## 代码实战

实现三种 grade 合并器和策略检查；证明 `approve;call` 与 `call;approve` 集合相同但 trace 判定不同。

## 与 DeepSeek Harness / LLM 工业应用的联系

权限策略常具有单调 guard 和顺序要求。选错 grade 会把关键安全信息压掉；后续读真实 tool pipeline 时将检查其显式事件顺序。

## 60 分钟安排

- 0–5：列出三种幺半运算。
- 5–25：精读 graded 类型。
- 25–45：运行 grade 对照。
- 45–55：完成 bind 推导和顺序反例。
- 55–60：验收。

## 验收标准

- grade 合并与所选幺半群一致。
- 顺序反例可复现。
- 能说明上界分析与精确 trace 的差异。

## 可选延伸

研究 effect quantales；不计入今晚。
