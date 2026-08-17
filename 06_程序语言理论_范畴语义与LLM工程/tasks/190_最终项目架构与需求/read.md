# 第190晚：最终项目——架构与可验证需求

## 目标与前置

- 目标：定义 mini harness 的组件边界、事件词汇、工具/LLM 端口与验收性质。
- 前置：第148–189晚。

## 计入 60 分钟的必读

| 分钟 | 材料 | 版本 | 精确范围 | 问题 |
|---:|---|---|---|---|
| 12 | [Agent runtime contracts](https://github.com/deepseek-ai/deepseek-harness/blob/47f943859bef60e4160492346772ded9b24f765a/packages/core/agent/src/runtime-types.ts#L38-L120) | Harness 47f943859bef60e4160492346772ded9b24f765a | path packages/core/agent/src/runtime-types.ts；L38–120；symbols AgentStatus、Agent；checked_at 2026-08-15 | 哪些能力属于端口而非实现？ |
| 8 | [AgentLoop publication](https://github.com/deepseek-ai/deepseek-harness/blob/47f943859bef60e4160492346772ded9b24f765a/packages/core/agent-loop/src/index.ts#L518-L603) | 同一 commit | path packages/core/agent-loop/src/index.ts；L518–603；symbols PreparedAgent.publish、createAgent、setupAndPublish；checked_at 2026-08-15 | 最终项目最小发布事务是什么？ |

## 阅读导引

写四张表：ports、durable events、effects/disposers、acceptance properties。需求必须可被有限断言证伪，例如“dispose 后 registry 无残留”，不要写“足够可靠”。

## 核心推导

架构由纯 core 与不可信边界组成：core 只依赖 Clock/Llm/Tool/Store 端口；所有边界输入为 unknown 并验证；所有资源注册返回 disposer；所有可恢复状态来自 event log。

## 工业联系与事实标签

- [THEOREM] 可执行性质比自然语言愿望更强：存在反例时断言给出有限见证。
- [EMPIRICAL] 固定 Harness 将 interface service 与 concrete agent-loop 分包。
- [INFERENCE] 端口化让 CI 使用 deterministic mock，部署替换真实 provider。
- [OPEN] 本课程 mini harness 不声称达到官方 Harness 的安全或并发覆盖。

## 严格 60 分钟

- 0–5：核对固定 SHA；5–25：必读；25–35：运行 `practice.ts` 契约预检；35–55：在真实 checkout 新建 `packages/examples/course-capstone`（package.json、src/index.ts、src/index.spec.ts），真实 import `@deepseek-ai/cordis` 并运行定向 Vitest；55–60：保存 SHA、diff 与测试输出。

## 验收

`practice.ts` 覆盖四端口、六事件及合法/非法/空计划；真实 checkout 中存在可由 workspace 解析的 capstone package，定向 Vitest 通过，并提交 SHA、diff、命令和输出。两部分缺一不可。

## 可选延伸

加入威胁模型与 SLO，不计时。
