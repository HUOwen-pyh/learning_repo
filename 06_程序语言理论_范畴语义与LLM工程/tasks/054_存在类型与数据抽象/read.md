# 第 054 晚：存在类型与表示独立性

## 具体目标

- 实现 existential package 的 witness 替换检查。
- 区分接口类型与隐藏表示类型。
- 用两个不同表示验证客户端观察不到实现差异。

## 前置编号

- 必须完成：053
- 开始前应能回答：`∀α` 是使用者选择类型，`∃α` 又是谁选择？

## 必读（20 分钟，计入本晚 60 分钟）

| 分钟 | 材料与版本 | 精确章节、页码或页内标题 | 带着什么问题读 |
|---:|---|---|---|
| 5–15 | [Cambridge Topics in Type Systems 2024–25](https://www.cl.cam.ac.uk/teaching/2425/Types/materials.html) | Lecture 6 “Existential types, data abstraction, termination of System F”，existential package/unpack 部分 | unpack 时为何不能让隐藏 witness 类型逃逸到结果类型？ |
| 15–25 | [Mitchell & Plotkin, Abstract Types Have Existential Type（ACM 原始论文）](https://doi.org/10.1145/41625.41628) | §2 “Existential types” 与 §3 的 abstraction interpretation | 一个模块的私有表示怎样由 existential witness 表达？ |

以上链接直接指向教材作者、大学课程或原始论文；阅读只到表中边界，不顺延挤占实战时间。

## 导读

`pack [B,v] as ∃α.A` 由提供者选择 witness `B`，但客户端只能按公开的 `A` 使用值。消去规则的逃逸条件是表示独立性的语法防线。今天的脚本聚焦 pack 检查和不透明客户端，而非完整高阶模块系统。

## 今晚必须完成的推导或证明

为 `pack [Nat, 0] as ∃α.α` 写 typing derivation；再解释为何 `unpack α,x=p in x` 不能被赋予结果类型 `α`。

把推导写在纸上或个人笔记中；关键规则名、每一步产生的约束以及失败位置必须可复查，不能只记录最终答案。

## 与 DeepSeek Harness / LLM 工程的联系

Harness service 定义是公开接口，provider 内部状态是隐藏表示。存在类型给出“可替换实现、客户端不依赖表示”的严格模型。

这里的联系是工程建模用途，不声称 Harness 直接实现了本节全部形式系统。

## 严格 60 分钟

| 时间 | 动作 | 到点产物 |
|---:|---|---|
| 0–5 | 闭卷回忆前置概念并写一个例子 | 一条定义和一个反例 |
| 5–25 | 完成上表两段必读 | 两个阅读问题的短答 |
| 25–38 | 完成指定推导/证明 | 可逐步检查的推导 |
| 38–55 | 阅读并运行 `practice.py`，完成动手改造 | 全部断言通过 |
| 55–60 | 对照验收清单，写下一个未解决问题 | 验收记录 |

总计严格为 60 分钟；可选延伸不属于今晚预算。

## 验收

- [ ] 能说明 existential 的选择权属于 producer。
- [ ] 脚本接受两个合法表示，拒绝 witness/value 不匹配。
- [ ] 动手改造：把接口从单值扩成 `(make, observe)` 操作对。

## 可选延伸（不计入 60 分钟）

阅读 Mitchell–Plotkin §4 的 representation independence 讨论。

