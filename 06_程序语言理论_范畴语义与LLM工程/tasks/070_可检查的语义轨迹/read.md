# 第 070 晚：周验收：可检查的小步语义轨迹

## 具体目标

- 生成带规则名的完整小步 trace。
- 独立验证每条相邻边和最终 normal form。
- 拒绝跳步、伪造规则名和正常形之后的额外事件。

## 前置编号

- 必须完成：064–069
- 入口检查：为什么 `[初始项, 最终值]` 通常不是充分的执行证明？

## 必读表（20 分钟，计入总计）

| 分钟 | 开放权威材料及版本 | 精确章节/页码/页内标题 | 阅读问题 |
|---:|---|---|---|
| 5–15 | [Cambridge, Semantics of Programming Languages 2025–26 官方讲义](https://www.cl.cam.ac.uk/teaching/2526/Semantics/notes.pdf) | §2.1 pp.13–23 的 transition closure；§3 pp.33–48 的 proof principles | 一条多步 judgement 能怎样分解成逐边可检查证据？ |
| 15–25 | [Software Foundations PLF 7.0，Smallstep](https://softwarefoundations.cis.upenn.edu/plf-current/Smallstep.html) | “Multi-Step Reduction” 中 `multi`, `multi_R`, `multi_trans` | 零步、一步和传递拼接分别由哪个构造器表达？ |

材料均来自大学官方课程或教材官方站点；PDF 页码以讲义印刷页码为准。

## 导读

执行器和验证器必须分开：前者产生 trace，后者只信任规则定义。这样日志来自不可信组件时仍能复核。脚本还保留零步 trace，体现多步闭包的自反性。

## 今晚推导 / 证明

证明若每条相邻边满足单步关系，则列表首尾满足多步关系；对列表长度归纳，并处理单元素边界。

推导必须写出配置、规则名与规则前提；只写最终值不合格。

## Harness / LLM 联系

Harness session log 是模型上下文的 durable source。若每条事件都能由统一 transition function replay，就可以检测日志缺口、非法重排与重复提交。

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

- [ ] 生成器产生的 trace 被独立 checker 接受。
- [ ] checker 拒绝跳步、错误规则和非 normal 终点。
- [ ] 动手改造：为每条边加入前一条摘要，构造 hash chain。

## 可选延伸（不计入 60 分钟）

将 trace 编码成 JSON，再从 JSON 恢复并验证。

