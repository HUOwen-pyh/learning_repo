# 第 116 晚：从伴随构造 Monad

## 学习目标

- 从 `F⊣G` 构造端函子 `T=GF`、单位 `η` 和乘法 `μ=GεF`。
- 把三角恒等式转换成 Monad 的单位律与结合律。

## 前置知识与关联任务

需要 114 的单位/余单位、106 的函子复合和 112 的幺半结构。

## 必读材料（计入今晚 60 分钟）

| 分钟 | 材料 | 版本 | 精确范围 | 带着什么问题读 |
|---:|---|---|---|---|
| 14 | [Riehl, Category Theory in Context](https://emilyriehl.github.io/files/context.pdf) | author PDF | §5.1，从 monad definition 至“monad induced by an adjunction”构造 | `μ:T²→T` 为什么含有余单位而不是单位？ |
| 6 | 同书 | author PDF | §5.1 的 Monad laws 图表 | 两条单位律和结合律分别压平什么嵌套？ |

## 精读导引

Monad 是一个端函子加自然变换 `η:Id→T`、`μ:T²→T`，满足三条图表。这里“Monad 是端函子范畴中的幺半群对象”是精确数学陈述；它不等于“Monad 就是普通集合上的半群”。从伴随得到的 `μ` 先在中间用 `ε:FG→Id_D` 消去一层自由—遗忘往返。

## 必须完成的推导或证明

逐类型检查 `GεF:GFGF→GF`。选一条 Monad 单位律，标明它对应哪条三角恒等式。

## 代码实战

以列表 Monad 的 singleton 和 flatten 表示 `η,μ`，验证两条单位律与结合律；错误 flatten 丢空列表时给出反例。

## 与 DeepSeek Harness / LLM 工业应用的联系

Monad 为状态、失败和异步计算提供组合语义；Cordis 自身以可撤销 effect/coeffect 形式化，不应把两者混成同一个源码机制。

## 60 分钟安排

- 0–5：写伴随的 unit/counit 类型。
- 5–25：精读构造与图表。
- 25–45：运行列表 `η/μ` 定律测试。
- 45–55：完成 `GεF` 类型推导。
- 55–60：验收。

## 验收标准

- 精确写出 `T,η,μ`。
- 三条 Monad 定律均有可执行实例。
- 能清楚说出 Monad 与 Cordis effect 的差异。

## 可选延伸

研究 monadicity；不计入今晚。
