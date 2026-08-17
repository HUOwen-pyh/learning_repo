# 第 034 晚：Church 数与高阶数据编码

## 学习目标

- 将自然数理解为函数迭代次数。
- 推导 successor、addition、multiplication。
- 写出编码/解码测试并识别成本边界。

## 前置任务

- 第 033 晚“Church 布尔与控制编码”。

## 必读材料（计入今晚 60 分钟）

| 分钟 | 材料 | 版本 | 精确范围 | 带着问题读 |
|---:|---|---|---|---|
| 16 | [PLFA — Untyped](https://plfa.github.io/22.08/Untyped/) | 22.08 | “Test examples”：`twoᶜ`、`fourᶜ`、`plusᶜ` 及解释段落 | `plus` 如何串联两段迭代？ |
| 9 | [PLFA — Untyped](https://plfa.github.io/22.08/Untyped/) | 22.08 | “Naturals and fixpoint” 开头 Church 与 Scott numerals 对比，至 Scott `two` | 不同编码让哪个操作便宜/昂贵？ |

## 精读导引

把 `n` 读成 `λf.λx.f^n(x)`。加法是先做 n 次再做 m 次；乘法让“做 n 次”本身重复 m 次。用 `f(x)=x+1, x=0` 解码只是观察编码，不是其定义。

## 必须完成的推导

1. β 推导 `succ zero` 的行为是一轮迭代。
2. 展开 `plus two three f x` 得到五次 `f`。
3. 说明 Church predecessor 为何比 successor 复杂，并与 Scott 编码对比。

结论类型：【表示/复杂度提醒】同一抽象数据可有不同消去成本；编码选择影响运行代价。

## 与 DeepSeek Harness / LLM 工业应用的联系

这是基础但重要的建模联系：接口能表达某对象，不代表关键操作高效。设计 LLM 工具协议时要同时评估表示能力、序列化长度和常用操作成本。

## 60 分钟安排

| 环节 | 分钟 |
|---|---:|
| 必读材料 | 25 |
| successor/add/mul 推导 | 13 |
| 完成高阶编码 | 18 |
| 验收 | 4 |
| **合计** | **60** |

## 验收标准

- 能从定义解释“数字就是迭代器”。
- `2+3`、`2×3` 解码正确。
- 零边界和非法编码反例被测试。

## 可选延伸

- 实现 pair-accumulator 版本 predecessor，并统计调用次数。

