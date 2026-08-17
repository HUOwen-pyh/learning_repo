# 第 056 晚：Algorithm W 周验收：主类型推断

## 具体目标

- 整合新鲜变量、实例化、泛化、替换和合一。
- 为 lambda/application/let 推断主类型。
- 用 self-application 检验 occurs check，用多态 id 检验 let-generalization。

## 前置编号

- 必须完成：050–055
- 开始前应能回答：W 在变量、lambda、应用、let 四种节点分别返回什么？

## 必读（20 分钟，计入本晚 60 分钟）

| 分钟 | 材料与版本 | 精确章节、页码或页内标题 | 带着什么问题读 |
|---:|---|---|---|
| 5–15 | [Damas & Milner, Principal type-schemes for functional programs](https://doi.org/10.1145/582153.582176) | §3 “The type assignment algorithm W” 与 Theorem 2 | W 的返回替换为何必须立即作用到环境和后续类型？ |
| 15–25 | [PLFA，`Inference`](https://plfa.inf.ed.ac.uk/Inference/) | “Inference” 章中 constraints、unification、inference 汇合部分 | 从语法生成约束再合一，与直接在线执行 W 有何对应？ |

以上链接直接指向教材作者、大学课程或原始论文；阅读只到表中边界，不顺延挤占实战时间。

## 导读

Algorithm W 是本周所有局部机制的组合测试。关键不是输出字符串，而是替换组合的方向、环境更新时机和 let 泛化边界。脚本使用确定性变量命名，便于逐步对照手算。

## 今晚必须完成的推导或证明

手算 `let id = λx.x in id id` 的 W 轨迹：列出每个新鲜变量、约束、合一子、泛化模式和最终主类型。

把推导写在纸上或个人笔记中；关键规则名、每一步产生的约束以及失败位置必须可复查，不能只记录最终答案。

## 与 DeepSeek Harness / LLM 工程的联系

LLM 工具 DSL 若要从组合表达式推出 schema，也需要“局部产生约束、全局求最一般解”。保留 principal result 比过早固定成某个提供者类型更利于插件复用。

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

- [ ] 成功推断 identity、constant 与 let-polymorphic self-use。
- [ ] 拒绝 `λx. x x`，并确认是 occurs check 失败。
- [ ] 动手改造：加入 Bool literal，并使 `let id=...` 同时用于 Int 和 Bool。

## 可选延伸（不计入 60 分钟）

把 W 的 soundness 与 completeness 分开陈述；不要求今晚完成形式证明。

