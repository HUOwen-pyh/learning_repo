# 第 118 晚：Eilenberg–Moore 代数

## 学习目标

- 定义 Monad 代数 `a:TA→A` 及其单位/结合图表。
- 区分“按一种方式解释 effect”与“只构造 effectful computation”。

## 前置知识与关联任务

需要 116 的 `η,μ` 和 115 的幺半群 fold。

## 必读材料（计入今晚 60 分钟）

| 分钟 | 材料 | 版本 | 精确范围 | 带着什么问题读 |
|---:|---|---|---|---|
| 14 | [Riehl, Category Theory in Context](https://emilyriehl.github.io/files/context.pdf) | author PDF | §5.2 “Eilenberg–Moore category”，algebra 定义及两条图表 | `a∘η=id` 与 `a∘μ=a∘Ta` 各排除什么解释器？ |
| 6 | 同书 | author PDF | list/free-monoid monad 的 algebra 示例 | 为什么 list algebra 等价于幺半群结构？ |

## 精读导引

`T A` 是带计算结构的 `A`，代数 `a` 负责消解结构。单位律说纯值解释后不变；结合律说先压平嵌套再解释，等于逐层解释。对 List Monad，选择 `a:list A→A` 且满足定律正是选择单位和结合运算。

## 必须完成的推导或证明

以整数求和证明空表/单元素/嵌套列表满足两条 algebra 律；构造平均值解释器违反结合律的反例。

## 代码实战

通用 law checker 比较 sum、product 与 mean 三个 list algebra 候选，自动找到 mean 的反例。

## 与 DeepSeek Harness / LLM 工业应用的联系

把一串 event fold 成 surface 是“解释累积结构”的候选；代数律提示分批处理与一次处理应一致。真实 session projection 还含顺序和合法性不变量，不能只靠本例证明。

## 60 分钟安排

- 0–5：写 `η,μ` 类型。
- 5–25：精读 EM algebra。
- 25–45：运行 law checker。
- 45–55：完成 sum 证明和 mean 反例。
- 55–60：验收。

## 验收标准

- 写对两条 algebra 律。
- sum/product 通过且 mean 失败。
- 能解释 Kleisli 与 EM 两种视角差别。

## 可选延伸

阅读 comparison functor；不计入今晚。
