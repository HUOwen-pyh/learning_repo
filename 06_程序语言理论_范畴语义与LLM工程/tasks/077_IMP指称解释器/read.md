# 第 077 晚：周验收：IMP 的循环指称解释器

## 具体目标

- 整合表达式和命令的组合式指称。
- 以 approximant/fuel 观察终止与发散。
- 验证顺序、false-loop 边界和 factorial 示例。

## 前置编号

- 必须完成：071–076
- 入口问题：命令语义为何是 partial state transformer，而不总是 `State→State`？

## 必读（20 分钟，计入 60 分钟）

| 分钟 | 开放权威一手材料与版本 | 精确页码与章节 | 阅读问题 |
|---:|---|---|---|
| 5–15 | [Andrew M. Pitts, Denotational Semantics（Cambridge 官方讲义）](https://www.cl.cam.ac.uk/teaching/1112/DenotSem/dens-notes-bw.pdf) | §1.1–§1.2 pp.2–12，表达式、命令、while fixed point 的完整定义 | 赋值、顺序和 while 的组合子分别怎样变换状态？ |
| 15–25 | [Andrew M. Pitts, Denotational Semantics（Cambridge 官方讲义）](https://www.cl.cam.ac.uk/teaching/1112/DenotSem/dens-notes-bw.pdf) | §2.3–§2.4 pp.19–31，continuous function 与 least fixed point | 完整 while 语义为何选择最小不动点而非任意不动点？ |

版本固定为 Pitts 的 Cambridge 2011–12 课程讲义发布版；页码采用正文印刷页码。到点停止，不把后续章节算作“已经读过”。

## 导读

完整实现把表达式解释为状态到值，命令解释为可能未定义的状态变换。Python 用 `None` 和有限 fuel 观察近似；数学语义则是连续函数最小不动点。

## 必做推导 / 证明

展开 factorial 程序前两轮的状态变换；写出 `while true do skip` 的每个有限近似为何都在初始状态未定义。

必须写出序、函数空间或不动点中的对象类型；不能把数学上的 bottom 与 Python 的偶然异常混为一谈。

## Harness / LLM 工程联系

一个 tool workflow 也可组合成 state transformer；显式 partiality 迫使工程区分正常结果、预算耗尽、取消和真正失败，而不是都压成空字符串。

这里只使用组合性、近似和不动点作为分析工具，不声称 Harness 以该指称模型实现。

## 严格 60 分钟

| 时段 | 动作 |
|---:|---|
| 0–5 | 闭卷写入口问题的定义与反例 |
| 5–25 | 完成两段精读和阅读问题 |
| 25–38 | 手算本晚推导/证明 |
| 38–55 | 运行并按顶部说明改造 `practice.py` |
| 55–60 | 完成验收，写一条不变量 |

总计 5 + 20 + 13 + 17 + 5 = 60 分钟。

## 验收

- [ ] factorial(4) 得到 24。
- [ ] false guard 零轮返回原状态，true/skip 在有限近似中未定义。
- [ ] 动手改造：增加结果类型区分 Diverged、OutOfFuel、Error。

## 可选延伸（不计入 60 分钟）

为无 while 的命令与操作解释器做 differential test。
