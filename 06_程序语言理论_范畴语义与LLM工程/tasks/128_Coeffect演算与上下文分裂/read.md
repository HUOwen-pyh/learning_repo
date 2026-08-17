# 第 128 晚：Coeffect 演算与上下文分裂

## 学习目标

- 阅读 coeffect typing judgment 中上下文注记的位置。
- 用组合算子计算复合表达式的总上下文需求。

## 前置知识与关联任务

需要 127 的 effect/coeffect 区分、061–070 的判断规则和 015–021 的代数组合。

## 必读材料（计入今晚 60 分钟）

| 分钟 | 材料 | 版本 | 精确范围 | 带着什么问题读 |
|---:|---|---|---|---|
| 16 | [Coeffects](https://tomasp.net/academic/papers/coeffects/) | ICALP 2014 | 论文 §2，coeffect calculus 的 judgment 与 structural rules | weakening/contraction 如何改变需求注记？ |
| 4 | [Cordis Primer](https://github.com/deepseek-ai/deepseek-harness/blob/47f943859bef60e4160492346772ded9b24f765a/docs/cordis-primer.md) | `47f943…` | “Declare service dependency via inject”一项 | required service 的合并更像集合并还是多重集加法？ |

## 精读导引

不同 coeffect 系统有不同代数：服务依赖常可用集合并，变量使用次数可能用自然数加法，邻域需求可用范围组合。不能预设所有需求都是集合。先确定注记代数的单位、合并与缩放，再读 typing rule。

## 必须完成的推导或证明

为表达式 `pair(f(x),g(x,y))` 在“所需变量集合”和“变量使用次数”两种 coeffect 中各推一次；解释结果为何不同。

## 代码实战

实现 AST 上的变量需求集合和使用次数分析，检查 weakening 与 duplication 的最小反例。

## 与 DeepSeek Harness / LLM 工业应用的联系

Cordis service 依赖通常关心存在性，线性资源/一次性凭证则不能用简单集合。课程由此训练选择正确依赖代数。

## 60 分钟安排

- 0–5：写 coeffect judgment。
- 5–25：精读规则。
- 25–46：运行双分析器。
- 46–55：完成 pair 推导。
- 55–60：验收。

## 验收标准

- 能指出上下文注记的组合运算。
- 集合/次数分析输出不同且正确。
- 能说明 Cordis 依赖模型不自动覆盖线性资源。

## 可选延伸

研究 structural 与 flat coeffects；不计入今晚。
