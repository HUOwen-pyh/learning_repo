# 第 058 晚：一致性、可归约性与强规范化

## 具体目标

- 区分弱规范化、强规范化和求值器带 fuel 停止。
- 理解 STLC 规范化证明中 fundamental lemma 的结构。
- 实现类型检查后再规范化的安全入口。

## 前置编号

- 必须完成：057 与第 5–6 周 lambda/STLC 任务
- 闭卷入口问题：为什么“所有闭良类型项都规范化”蕴含某些类型没有闭 inhabitant？

## 必读（20 分钟，已计入 60 分钟）

| 分钟 | 开放权威一手材料与版本 | 精确章节、页码或页内标题 | 阅读问题 |
|---:|---|---|---|
| 5–15 | [Cambridge Topics in Type Systems 2024–25](https://www.cl.cam.ac.uk/teaching/2425/Types/materials.html) | Lecture 3 “Consistency and termination”，strong normalization 与 reducibility argument | 逻辑关系为何按类型结构定义，而非只按项大小归纳？ |
| 15–25 | [Software Foundations PLF 7.0，Norm](https://softwarefoundations.cis.upenn.edu/plf-current/Norm.html) | “Normalization” 章的 “Normal Forms and Normalization” 与 “Logical Relations” | 箭头类型的 reducibility candidate 对所有什么参数量化？ |

只读指定边界；链接均为大学官方讲义、作者版本或正式论文页面。

## 导读

测试若干项都会停止不是强规范化证明。标准证明先按类型定义可归约集合，再证明良类型替换保持可归约，最后推出闭良类型项终止。脚本用小步和 fuel 暴露“算法观察”与“数学定理”的差别。

## 必做推导 / 证明

写出 base 类型与 `A→B` 的 reducibility 定义；证明恒等函数属于 `R[A→A]` 的关键一步。

必须保留判断形式和规则名；“凭直觉显然”不算完成。

## DeepSeek Harness / LLM 工程联系

Agent loop 的步数上限只保证资源边界，不等于工作流语言本身规范化。若 DSL 排除一般递归，强规范化可提供比 timeout 更强的终止保证。

这是从形式概念到工程约束的映射；除明确指出外，不宣称 Harness 已静态证明这些性质。

## 严格 60 分钟

| 时间 | 工作 |
|---:|---|
| 0–5 | 回忆入口问题，写定义和反例 |
| 5–25 | 完成必读表并回答两个问题 |
| 25–38 | 手写推导或证明 |
| 38–55 | 运行 `practice.py`，再完成文件顶部的动手改造 |
| 55–60 | 按验收项自测并记录一个疑问 |

5 + 20 + 13 + 17 + 5 = 60 分钟。下面的延伸不得挤入本晚。

## 验收

- [ ] 能区分三种终止说法。
- [ ] 脚本正规化两个良类型项，并拒绝 self-application。
- [ ] 动手改造：加入 product 和投影的归约规则。

## 可选延伸（不计时）

继续 SF `Norm` 的 fundamental property 证明。

