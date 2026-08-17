# 第 072 晚：While 循环：递归语义与有限近似

## 具体目标

- 写出 while functional。
- 从 bottom 迭代有限近似。
- 区分“fuel 不够”与数学上的发散。

## 前置编号

- 必须完成：071
- 入口问题：为什么 while 的指称不能只靠语法子项做一次有限组合？

## 必读（20 分钟，计入 60 分钟）

| 分钟 | 开放权威一手材料与版本 | 精确页码与章节 | 阅读问题 |
|---:|---|---|---|
| 5–15 | [Andrew M. Pitts, Denotational Semantics（Cambridge 官方讲义）](https://www.cl.cam.ac.uk/teaching/1112/DenotSem/dens-notes-bw.pdf) | §1.2 “While-loops as fixed points” pp.7–12 | while functional 的不动点方程怎样展开一次循环？ |
| 15–25 | [Andrew M. Pitts, Denotational Semantics（Cambridge 官方讲义）](https://www.cl.cam.ac.uk/teaching/1112/DenotSem/dens-notes-bw.pdf) | §1.2 中 `w = F(w)`、有限 unfoldings 与 partial functions | 第 n 个近似知道最多多少轮循环的信息？ |

版本固定为 Pitts 的 Cambridge 2011–12 课程讲义发布版；页码采用正文印刷页码。到点停止，不把后续章节算作“已经读过”。

## 导读

循环语义是一个递归方程。第 0 近似完全未定义，第 n+1 近似可观察 guard，并把递归调用交给第 n 近似。近似链的上确界才是完整语义。

## 必做推导 / 证明

令 guard 为 `x>0`、body 为 `x:=x-1`，手算从 `x=2` 出发的 `W0,W1,W2,W3`，标明首次得到结果的层数。

必须写出序、函数空间或不动点中的对象类型；不能把数学上的 bottom 与 Python 的偶然异常混为一谈。

## Harness / LLM 工程联系

Agent loop 的 max-turn 是有限 unfolding。它能安全截断，但不是任务本身无穷行为的完整含义；两者在评测中必须分开标记。

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

- [ ] 能写 while functional 的类型和方程。
- [ ] 脚本显示近似随层数增加而定义更多输入。
- [ ] 动手改造：统计循环步数并保持结果不变。

## 可选延伸（不计入 60 分钟）

比较 operational unrolling 与 denotational approximants 的对应。
