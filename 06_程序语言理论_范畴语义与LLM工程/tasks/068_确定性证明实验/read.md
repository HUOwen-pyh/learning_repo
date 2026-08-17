# 第 068 晚：操作语义确定性：规则互斥与归纳证明

## 具体目标

- 定义关系确定性而非函数确定性。
- 枚举所有适用规则，检查后继至多一个。
- 故意加入重叠规则，构造非确定反例。

## 前置编号

- 必须完成：064、067
- 入口检查：“解释器每次只返回一个结果”为什么尚未证明规则关系确定？

## 必读表（20 分钟，计入总计）

| 分钟 | 开放权威材料及版本 | 精确章节/页码/页内标题 | 阅读问题 |
|---:|---|---|---|
| 5–15 | [Cambridge, Semantics of Programming Languages 2025–26 官方讲义](https://www.cl.cam.ac.uk/teaching/2526/Semantics/notes.pdf) | §3.3 “Example proofs” pp.47–48，operational semantics proof examples | 确定性证明对两棵以同一配置为根的推导做什么分析？ |
| 15–25 | [Software Foundations PLF 7.0，Smallstep](https://softwarefoundations.cis.upenn.edu/plf-current/Smallstep.html) | 定理 `step_deterministic` 及其前后的 determinism 定义 | 哪些规则对的结论形状可能重叠，如何排除？ |

材料均来自大学官方课程或教材官方站点；PDF 页码以讲义印刷页码为准。

## 导读

把语义直接写成 Python 函数会隐藏“是否有第二条规则也适用”。今晚让每条规则独立返回候选后继，再检查集合大小，从而逼近论文中的规则重叠分析。

## 今晚推导 / 证明

假设 `e→e1` 且 `e→e2`，按第一棵推导最后规则归纳，完成 Add-left/Add-right/Add-value 三类的关键互斥论证。

推导必须写出配置、规则名与规则前提；只写最终值不合格。

## Harness / LLM 联系

多个 Harness 插件可能都声称处理同一 waterfall 事件。显式优先级是有意选择；未声明的重叠则类似非确定语义，会破坏 replay。

## 严格 60 分钟

| 时段 | 任务 | 输出 |
|---:|---|---|
| 0–5 | 闭卷回答入口问题 | 定义和一个反例 |
| 5–25 | 按必读表精读 | 两个问题各 2–3 句 |
| 25–38 | 完成推导/证明 | 可检查的规则树或归纳步骤 |
| 38–55 | 运行并改造 `practice.py` | 正反/边界断言全通过 |
| 55–60 | 按验收清单复盘 | 一条不变量和一个疑问 |

合计 5 + 20 + 13 + 17 + 5 = 60 分钟。

## 验收

- [ ] 能写出关系确定性的量词定义。
- [ ] 标准规则集每项至多一个后继。
- [ ] 动手改造：加入一个重叠规则，输出最小非确定反例。

## 可选延伸（不计入 60 分钟）

比较 nondeterministic semantics 与实现层 race condition，记录它们不等同之处。

