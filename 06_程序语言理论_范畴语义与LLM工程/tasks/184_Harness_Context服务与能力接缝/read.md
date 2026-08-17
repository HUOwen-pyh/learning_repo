# 第184晚：Harness Context 服务与能力接缝

## 目标与前置

- 目标：审计 Agent 接口、factory/handle 所有权与 Context capability seam。
- 前置：结构类型、依赖注入、event sourcing。

## 计入 60 分钟的必读

| 分钟 | 材料 | 版本 | 精确范围 | 问题 |
|---:|---|---|---|---|
| 10 | [agent/runtime-types.ts](https://github.com/deepseek-ai/deepseek-harness/blob/47f943859bef60e4160492346772ded9b24f765a/packages/core/agent/src/runtime-types.ts#L38-L120) | Harness 47f943859bef60e4160492346772ded9b24f765a | path packages/core/agent/src/runtime-types.ts；L38–L120；symbols AgentStatus、Agent、cancel/whenIdle/send；checked_at 2026-08-15 | 什么是稳定能力，什么是驱动实现？ |
| 15 | [agent/src/index.ts](https://github.com/deepseek-ai/deepseek-harness/blob/47f943859bef60e4160492346772ded9b24f765a/packages/core/agent/src/index.ts#L149-L241) | 同一 commit | path packages/core/agent/src/index.ts；定向读 L149–203 与 L230–241；symbols AgentHandle、AgentFactory.createAgent/resume、AgentRegistry；checked_at 2026-08-15 | 消费者为何只依赖 `ctx.agents` 而不 import AgentLoop？ |

## 阅读导引

列出 Service Definition (`AgentRegistry`/`AgentFactory`)、Provider (`AgentLoop`)、Consumer 三列，再沿 `AgentHandle.dispose` 记录所有权。今晚不读 runtime-context projection，避免与「能力接缝」标题错配。

## 核心推导

capability seam 以小接口隔离 provider：`AgentRegistry` 暴露查找/创建能力，`AgentFactory` 提供实现，`AgentHandle.dispose` 则把 teardown 权限交给调用方。消费者不需要知道 AgentLoop 的具体类。

## 工业联系与事实标签

- [THEOREM] 若消费者只依赖 capability interface，则替换满足同一契约的 provider 不改变消费者的类型依赖。
- [EMPIRICAL] 固定源码把 `AgentRegistry`、`AgentFactory` 与 `AgentHandle` 分开，并由 handle 暴露 dispose 所有权。
- [INFERENCE] 工业插件应依赖 AgentFactory/Context service，不命名具体 ReactLoopAgent。
- [OPEN] 跨进程 provider 的 capability ownership 需 RPC lease/heartbeat 扩展。

## 严格 60 分钟

- 0–5：核对固定 SHA；5–30：精读两个局部行段；30–40：运行 `practice.ts` 能力替换预检；40–55：在真实 checkout 用 `rg "AgentFactory|setFactory|createAgent" packages/core` 追出 definition/provider/consumer，保存三列表；55–60：记录一条 disposer 所有权链。

## 验收

`practice.ts` 替换/缺失断言通过；真实 checkout 三列表含 path/symbol/line/owner；能解释 `AgentHandle` 为何是 teardown capability。

## 可选延伸

检索固定提交中 ReactLoopAgent 是否从包根导出，不计时。
