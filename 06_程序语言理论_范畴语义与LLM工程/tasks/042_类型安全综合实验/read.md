# 第 042 晚：类型安全综合实验

## 学习目标

- 将 progress 与 preservation 组合成安全 evaluator。
- 区分 rejected、done 与 out-of-gas。
- 用测试语料检查每一步的类型不变量与非 stuck 性。

## 前置任务

- 第 036–041 晚全部任务。

## 必读材料（计入今晚 60 分钟）

| 分钟 | 材料 | 版本 | 精确范围 | 带着问题读 |
|---:|---|---|---|---|
| 14 | [PLFA — Properties](https://plfa.github.io/22.08/Properties/) | 22.08 | Introduction 中“recipe for automating evaluation”完整段落 | progress 与 preservation 各负责循环中的哪一步？ |
| 12 | [PLFA — Properties](https://plfa.github.io/22.08/Properties/) | 22.08 | “Evaluation” 从 Gas/Finished 到 evaluator type signature 和前三个 cases | evaluator 的返回类型怎样携带安全证据？ |

## 精读导引

循环不变量是：当前项闭、类型始终为初始 T。progress 保证它若非值就有下一步；preservation 把不变量送到下一轮。类型安全不等于 termination，所以 API 仍保留 out-of-gas。

## 必须完成的推导

1. 写出 `well-typed ⇒ not stuck` 如何由两 theorem 合成。
2. 对多步关系归纳推出每个中间项同类型。
3. 列出类型安全不保证的三件事：终止、无 I/O 失败、业务结果正确。

结论类型：【类型安全定理】闭且良类型 STLC 项不会 stuck；【边界】该结论不包含终止或外部副作用成功。

## 与 DeepSeek Harness / LLM 工业应用的联系

直接联系：安全 runner 应先校验、逐步维护协议不变量、明确预算耗尽，并把类型安全与任务正确率分开报告。这是后续 typed tool-calling harness 的核心设计骨架。

## 60 分钟安排

| 环节 | 分钟 |
|---|---:|
| 必读材料 | 26 |
| 安全循环推导 | 11 |
| 完成综合 runner | 19 |
| 验收 | 4 |
| **合计** | **60** |

## 验收标准

- runner 对 ill-typed 输入在执行前拒绝。
- typed 输入每步同类型且不会 stuck。
- done 正例、rejected 反例、零步值边界均通过。

## 可选延伸

- 有界生成深度 3 的闭项，做自动化 progress/preservation 回归。

