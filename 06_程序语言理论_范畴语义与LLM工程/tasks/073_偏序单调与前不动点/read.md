# 第 073 晚：偏序、单调函数与前不动点

## 具体目标

- 实现有限偏序公理检查。
- 检查函数单调性、前不动点和最小元素。
- 构造一个非单调反例。

## 前置编号

- 必须完成：072
- 入口问题：`f(x) ≤ x` 与 `f(x)=x` 分别叫什么，前者为什么更弱？

## 必读（20 分钟，计入 60 分钟）

| 分钟 | 开放权威一手材料与版本 | 精确页码与章节 | 阅读问题 |
|---:|---|---|---|
| 5–15 | [Andrew M. Pitts, Denotational Semantics（Cambridge 官方讲义）](https://www.cl.cam.ac.uk/teaching/1112/DenotSem/dens-notes-bw.pdf) | §2.1 “Partially ordered sets and monotone functions” pp.13–16 | 偏序的三条公理各排除什么异常关系？ |
| 15–25 | [Andrew M. Pitts, Denotational Semantics（Cambridge 官方讲义）](https://www.cl.cam.ac.uk/teaching/1112/DenotSem/dens-notes-bw.pdf) | §2.2 “Least elements and least pre-fixed points” pp.16–18 | 最小前不动点怎样蕴含最小不动点？ |

版本固定为 Pitts 的 Cambridge 2011–12 课程讲义发布版；页码采用正文印刷页码。到点停止，不把后续章节算作“已经读过”。

## 导读

语义近似按“信息更多”排序，而不必按数值大小。单调性保证增加输入信息不会减少输出信息。Tarski 风格结论关注最小前不动点，再推出它也是不动点。

## 必做推导 / 证明

在 powerset 格上令 `F(X)={s}∪post(X)`，证明 F 单调；写出所有 pre-fixed points 必须满足的闭包条件。

必须写出序、函数空间或不动点中的对象类型；不能把数学上的 bottom 与 Python 的偶然异常混为一谈。

## Harness / LLM 工程联系

权限/能力集合天然按包含排序。声明更多可用 service 后，合法分析不应反而丢失已有结果；这是一种单调性设计检查。

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

- [ ] 偏序检查覆盖自反、反对称、传递。
- [ ] 脚本区分 monotone 与 complement 反例。
- [ ] 动手改造：改用 divisibility poset。

## 可选延伸（不计入 60 分钟）

为一个 finite poset 画 Hasse diagram。
