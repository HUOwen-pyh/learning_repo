# 第 082 晚：组合性与操作—指称可靠性

## 具体目标

- 在同一表达式上实现操作和指称两个解释器。
- 穷举小规模 AST 做 differential check。
- 区分测试证据与一般 soundness 定理。

## 前置编号

- 必须完成：078、080–081
- 入口问题：soundness 要从操作 judgement 推出哪一个指称等式？

## 必读表（20 分钟，计入总时长）

| 分钟 | 开放权威一手材料与版本 | 精确章节、页码或锚点 | 阅读问题 |
|---:|---|---|---|
| 5–15 | [Andrew M. Pitts, Denotational Semantics（Cambridge 官方讲义）](https://www.cl.cam.ac.uk/teaching/1112/DenotSem/dens-notes-bw.pdf) | §§6.3–6.4 pp.77–80：“Compositionality” 与 “Soundness” | 一小步保持 denotation 与最终求值可靠性有何关系？ |
| 15–25 | [PLFA，Soundness](https://plfa.inf.ed.ac.uk/Soundness/) | `Soundness` 章中 denotational soundness theorem 及 proof structure | 证明为什么对求值推导归纳，而不是枚举测试？ |

Pitts PDF 固定为 Cambridge 2011–12 课程讲义发布版；网页采用当前公开章版。页码按正文印刷页，只读规定范围。

## 导读

可靠性通常说操作语义认可的计算不会改变指称含义。两个独立实现的 differential test 很有用，但共同 bug 或有限覆盖仍可能漏错，所以还需归纳证明。

## 必做推导或证明

对 Add 语言证明：若 `e→e'`，则 `⟦e⟧=⟦e'⟧`；按最后规则分三种情况。

证明要明确量化的是所有程序、所有上下文还是本脚本的有限样本；三者不能混写。

## Harness / LLM 工程联系

在线执行与 session replay projection 应是两种独立路径；对同一 trace 的结果做 differential test 能发现事件遗漏或顺序错误。

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

- [ ] 所有深度≤2样本的操作结果等于指称结果。
- [ ] 故意错误的减法解释被反例捕获。
- [ ] 动手改造：输出最小反例 AST。

## 可选延伸（不计入 60 分钟）

加入变量环境后重做有限枚举。
