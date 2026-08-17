# 第 028 晚：de Bruijn 移位、替换与周项目

## 学习目标

- 实现带 cutoff 的 de Bruijn `shift`。
- 实现单变量替换并完成一次 β 收缩。
- 解释进入 binder 时索引为何必须同步调整。

## 前置任务

- 第 027 晚“de Bruijn 索引与作用域”。

## 必读材料（计入今晚 60 分钟）

| 分钟 | 材料 | 版本 | 精确范围 | 带着问题读 |
|---:|---|---|---|---|
| 13 | [PLFA — DeBruijn](https://plfa.github.io/22.08/DeBruijn/) | 22.08 | “Renaming”：`ext` 与 `rename` 定义及 examples | 穿过 lambda 时为何保留 0、抬升其余索引？ |
| 12 | [PLFA — DeBruijn](https://plfa.github.io/22.08/DeBruijn/) | 22.08 | “Simultaneous Substitution” 与 “Single substitution”，读到 single substitution example 结束 | 单替换为何可由 simultaneous substitution 特化？ |

## 精读导引

先把 `shift(d,c,t)` 解释为“只移动索引 ≥ cutoff 的自由于当前局部上下文的变量”。进入 `λ` 时 cutoff 加一。β 收缩 `((λ.t) s)` 的标准三步是：抬升 `s`、替换 `#0`、整体下移。

## 必须完成的推导

1. 手算 `shift(1,0, λ.(#1 #0)) = λ.(#2 #0)`。
2. 手算 `((λ.#0) a) → a` 的三步过程。
3. 解释若进入 lambda 时 cutoff 不加一，会错误移动 binder 自己的 `#0`。

结论类型：【基础算法】移位维护索引相对 binder 的不变量，是无名替换正确性的关键。

## 与 DeepSeek Harness / LLM 工业应用的联系

这是基础层联系：该项目训练“表示不变量 + 局部变换 + 可执行断言”。Harness 的消息重写、工具轨迹变换也需要保持引用关系，但本晚不把 de Bruijn 机制直接等同于 Harness 实现。

## 60 分钟安排

| 环节 | 分钟 |
|---|---:|
| 必读材料 | 25 |
| 三步 β 推导 | 10 |
| 完成周项目代码 | 21 |
| 验收 | 4 |
| **合计** | **60** |

## 验收标准

- 能口述 cutoff 的含义。
- `shift` 不移动 binder 所绑定的局部索引。
- β 正例、非红ex反例、嵌套 binder 边界例全部通过。

## 可选延伸

- 把 `shift` 与 `subst` 的交换律写成小规模穷举属性测试。

