# 第161晚：可回放 Mock 工具 Agent 验收

## 目标与前置

- 目标：组合协议、agent、工具、评分与 append-only trace，得到无网络可重复测试台。
- 前置：第155–160晚。

## 计入 60 分钟的必读

| 分钟 | 材料 | 版本 | 精确范围 | 问题 |
|---:|---|---|---|---|
| 8 | [MCP Tools](https://modelcontextprotocol.io/specification/2025-11-25/server/tools) | 2025-11-25 | Security Considerations | 谁必须确认敏感工具调用？ |
| 7 | [Inspect Scoring](https://inspect.aisi.org.uk/scoring.html) | checked_at 2026-08-15 | Score、Explanation、Metadata | 失败诊断需保留什么？ |
| 5 | [τ-bench paper](https://openreview.net/pdf/57cd0f8d1f7b7790714c1bedf5d781ba10e56590.pdf) | ICLR 2025 | §3 Evaluation | 终态和沟通约束怎样共同评估？ |

## 阅读导引

把每次工具请求、策略拒绝、工具结果、最终回答写成不可变事件。回放只读取事件，不重新执行工具；否则回放可能再次产生副作用。

## 核心推导

事件日志 e1…en 经纯投影 fold(reduce, initial, events) 生成状态。只要 reducer 确定且版本固定，同一日志得到同一终态。工具执行与投影必须分离。

## 工业联系与事实标签

- [THEOREM] 确定性左折叠对相同初态和相同有序事件序列给出相同结果。
- [EMPIRICAL] benchmark 分数只表征既定任务、mock 与 scorer，不代表真实生产事故率。
- [INFERENCE] 可回放事件是调试、审计和离线评测的共同接口。
- [OPEN] 外部世界已改变时，历史工具结果的语义有效期需要领域规则。

## 严格 60 分钟

- 0–5：列事件；5–25：必读；25–50：运行 mock agent 与回放；50–57：篡改一条事件验证检测；57–60：写验收结论。

## 验收

成功、策略拒绝、空日志边界通过；回放不调用工具；事件包含单调序号。

## 可选延伸

加入哈希链和 trace schema 版本，不计时。
