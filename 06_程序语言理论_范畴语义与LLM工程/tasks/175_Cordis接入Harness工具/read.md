# 第175晚：Cordis 教程 7——接入 Harness 工具

## 目标与前置

- 目标：注册 defineTool、通过真实工具流水线执行、监听 tools/result，并理解三层契约。
- 前置：第153、158、168、169–174晚。

## 计入 60 分钟的必读

| 分钟 | 材料 | 版本 | 精确范围 | 问题 |
|---:|---|---|---|---|
| 20 | [Into the harness](https://github.com/deepseek-ai/deepseek-harness/blob/47f943859bef60e4160492346772ded9b24f765a/docs/cordis-tutorial/07-into-the-harness.md#L1-L107) | Harness 47f943859bef60e4160492346772ded9b24f765a | path docs/cordis-tutorial/07-into-the-harness.md；全章 L1–L107；symbols defineTool、ctx.tools.register/execute、tools/result、CallId；checked_at 2026-08-15 | canonical value、rendered content 和 event 分别服务谁？ |

## 阅读导引

跟踪输入参数 spec→JSON Schema→运行时验证→execute canonical value→output schema→render content→tools/result event。标出注册 disposer 与 inject tools/systemPrompt 的依赖。

## 核心推导

工具能力分三层：契约定义、执行流水线、观察/呈现。canonical value 用于程序语义，content 用于持久会话/模型，event 用于解耦观察者；混合会导致不可重放或 UI 细节污染逻辑。

## 工业联系与事实标签

- [THEOREM] 若 validator sound，则 execute 看到的参数满足其声明谓词；这不证明工具实现正确。
- [EMPIRICAL] 固定教程的 tools/result 在结果物化时发出，先于 execute Promise 向调用者返回。
- [INFERENCE] 审计插件应监听事件，不应修改工具实现或直接导入提供者。
- [OPEN] 工具副作用的事务性、授权和人工确认超出 schema 类型保证。

## 真实固定 checkout 实战

继续使用前六晚的同一教程工作区。按官方第七章创建 `greet-tool.ts`、`tool-logger.ts`，并在 `cordis.yml` 中装载 `@deepseek-ai/dsh-system-prompt`、`@deepseek-ai/dsh-tools` 与两个本地插件。运行真实 launcher，必须同时观察：工具实际执行、`tools/result` listener 先打印、调用者随后收到 rendered `content`。本章无须 API key。

随后沿用第 174 晚的稳定 id/HMR 机制，保留一个注入 `tools` 的 probe：卸载/禁用 `greet-tool` 后再次请求 `greet`，保存“工具不可用”的失败；卸载 `tool-logger` 后再运行一次已注册的控制工具或重新启用 `greet-tool`，确认不再出现该 listener 的日志。最终停止 watcher。注册、真实执行、事件、工具 disposer 和 listener disposer 五项都必须来自固定 checkout 的 Cordis/Harness 服务，而不是本地 registry 类。

## 严格 60 分钟

- 0–5：闭卷画 parameters→execute→canonical value→render→`tools/result`。
- 5–25：精读固定提交第七章 L1–L107。
- 25–37：运行本地 `practice.ts`，检查注册、校验、执行、事件与卸载断言。
- 37–44：在连续教程工作区按章创建真实工具、observer 与四项 composition。
- 44–49：运行真实 launcher，保存 `tools/result` 与 `tool replied` 的先后输出。
- 49–55：用稳定 id/HMR 与 probe 依次卸载工具、listener，记录工具不可调用和 listener 无残留后停止 watcher。
- 55–60：核对双门证据，整理七晚产物与周总结。

## 验收

- 本地门：`practice.ts` 的注册、执行、监听、卸载和非法参数断言全部通过。
- 真实门：固定 HEAD；真实 `defineTool` 注册与执行；`[tool-logger] greet -> Hello, Cordis!` 先于 `tool replied`；禁用工具后的不可调用失败；卸载 observer 后无其日志；watcher 已停止。证据必须含命令、退出/停止状态和关键输出。
- 两门必须同时通过；只运行本地 registry 或只复述 fixed path、symbol、commit 都不算完成本周。

## 可选延伸

阅读 examples/headless-agent/cordis.yml 的固定提交版本，不计时。
