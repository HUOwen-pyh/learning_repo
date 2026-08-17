# 第 083 晚：Adequacy：指称观察能否回到执行

## 具体目标

- 区分 soundness 与 computational adequacy。
- 实现 numeral value 与 semantic integer 的逻辑关系。
- 用终止/发散样本测试 adequacy 两个方向。

## 前置编号

- 必须完成：078–082
- 入口问题：soundness 的逆命题为什么通常更难？

## 必读表（20 分钟，计入总时长）

| 分钟 | 开放权威一手材料与版本 | 精确章节、页码或锚点 | 阅读问题 |
|---:|---|---|---|
| 5–15 | [Andrew M. Pitts, Denotational Semantics（Cambridge 官方讲义）](https://www.cl.cam.ac.uk/teaching/1112/DenotSem/dens-notes-bw.pdf) | Ch.7 “Relating denotational and operational semantics” pp.81–90 | logical relation 如何同时关联 semantic element 与 operational term？ |
| 15–25 | [PLFA，Adequacy](https://plfa.inf.ed.ac.uk/Adequacy/) | `Adequacy` 章的 logical relation、fundamental lemma 与 adequacy theorem | fundamental lemma 为何需要处理开放项和相关环境？ |

Pitts PDF 固定为 Cambridge 2011–12 课程讲义发布版；网页采用当前公开章版。页码按正文印刷页，只读规定范围。

## 导读

adequacy 说明指称不是凭空产生观察：若 denotation 表示一个可观察结果，程序也能求到对应值。一般证明需要按类型定义逻辑关系，再证明所有良类型项自相关。

## 必做推导或证明

写出 base Nat 和函数类型的逻辑关系；说明函数分支为什么量化所有相关输入。

证明要明确量化的是所有程序、所有上下文还是本脚本的有限样本；三者不能混写。

## Harness / LLM 工程联系

离线评测分数若不能对应可 replay 的实际轨迹，就缺少 adequacy 式保证。指标设计必须证明抽象分数与真实任务状态的关系。

## 严格 60 分钟

| 分钟 | 动作 |
|---:|---|
| 0–5 | 闭卷回答入口问题 |
| 5–25 | 精读两段材料并回答问题 |
| 25–38 | 完成推导/证明 |
| 38–55 | 运行及改造 `practice.py` |
| 55–60 | 对照验收并记录模型边界 |

合计严格为 60 分钟。

## 验收

- [ ] 脚本区分 undefined denotation 与 numeral result。
- [ ] 终止递归和发散递归得到符合预期的有限观察。
- [ ] 动手改造：加入 Bool 关系。

## 可选延伸（不计入 60 分钟）

比较 adequacy、completeness 和 full abstraction 三个术语。
