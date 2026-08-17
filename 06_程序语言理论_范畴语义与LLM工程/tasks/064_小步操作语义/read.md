# 第 064 晚：结构化小步操作语义

## 具体目标

- 把语法与单步关系分离。
- 实现算术表达式确定性的 CBV 小步。
- 区分 normal form、value 与 stuck。

## 前置编号

- 必须完成：第 4–6 周语法/Lambda 任务及 057–063
- 入口检查：值、正常形和 stuck term 是否是同一概念？

## 必读表（20 分钟，计入总计）

| 分钟 | 开放权威材料及版本 | 精确章节/页码/页内标题 | 阅读问题 |
|---:|---|---|---|
| 5–15 | [Cambridge, Semantics of Programming Languages 2025–26 官方讲义](https://www.cl.cam.ac.uk/teaching/2526/Semantics/notes.pdf) | §1 pp.8–12；§2.1 “Operational semantics” pp.13–23，配置与 transition rules | 小步关系的左右两侧为何是完整配置，而非只写表达式？ |
| 15–25 | [Software Foundations PLF 7.0，Smallstep](https://softwarefoundations.cis.upenn.edu/plf-current/Smallstep.html) | “A Toy Language” 至 “Multi-Step Reduction” | 单步闭包为多步关系时，零步情况为何必要？ |

材料均来自大学官方课程或教材官方站点；PDF 页码以讲义印刷页码为准。

## 导读

小步语义把一次可观察的计算拆成局部规则，因此能描述执行顺序、并发交错和错误位置。脚本用 `None` 表示无后继，但需要额外谓词区分“已经是值”与“错误地卡住”。

## 今晚推导 / 证明

为 `(1+2)+(3+4)` 写完整多步序列，每条边标注 `ST_Add1`、`ST_Add2` 或 `ST_AddConst`。

推导必须写出配置、规则名与规则前提；只写最终值不合格。

## Harness / LLM 联系

Agent turn 也可表示为配置间的小步：准备 prompt、模型流、工具请求、工具结果、提交日志。明确一步的原子边界有助于取消和 replay。

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

- [ ] 能给出 value/normal/stuck 的严格关系。
- [ ] 脚本覆盖普通归约、值边界和错误 operand。
- [ ] 动手改造：加入乘法且保持左到右求值。

## 可选延伸（不计入 60 分钟）

阅读 SF `Smallstep` 的 determinism 定理。

