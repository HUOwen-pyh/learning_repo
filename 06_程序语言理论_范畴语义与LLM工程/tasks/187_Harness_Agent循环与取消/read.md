# 第187晚：Harness Agent 循环、取消与 wake latch

## 目标与前置

- 目标：审计 idle/maintenance/running Phase、统一 send、取消、收敛与 wakeRequested 竞态。
- 前置：AbortSignal、状态机、异步竞态。

## 计入 60 分钟的必读

| 分钟 | 材料 | 版本 | 精确范围 | 问题 |
|---:|---|---|---|---|
| 13 | [agent.ts：收件箱与 latch](https://github.com/deepseek-ai/deepseek-harness/blob/47f943859bef60e4160492346772ded9b24f765a/packages/core/agent-loop/src/agent.ts#L104-L180) | Harness 47f943859bef60e4160492346772ded9b24f765a | path packages/core/agent-loop/src/agent.ts；L104–L180；symbols send/followup/steer/inject、cancel、runMaintenance、wakeDriver；checked_at 2026-08-15 | abort 后的 waking input 如何被改类并 latch？ |
| 12 | [agent.ts：收敛边界](https://github.com/deepseek-ai/deepseek-harness/blob/47f943859bef60e4160492346772ded9b24f765a/packages/core/agent-loop/src/agent.ts#L194-L311) | 同一 commit | path packages/core/agent-loop/src/agent.ts；定向读 L194–207、L227–311；symbols kick、turn、wakeRequested replay；checked_at 2026-08-15 | driver 何时原子读取并清除 latch？ |

## 阅读导引

画三态和信号所有权。对 followup/steer/inject 写 target×wakeup 表；定位 cancel 清 inbox、abort 当前信号、disposed 不 latch 与收敛边界重放。

## 核心推导

取消是合作式：发 signal 后必须等待已开始工作 drain。窗口期来的 waking input 设置 latch；driver 到 idle 边界读取 latch 再开新轮，避免 lost wakeup。

## 工业联系与事实标签

- [THEOREM] 在本晚状态机中，若 running 时 wake 设置 latch 且 convergence 原子读取/清除，唤醒不会在该窗口丢失。
- [EMPIRICAL] 固定源码明确 disposed cancel 不 latch，idle wake 总会打开 turn boundary。
- [INFERENCE] 工具/模型适配器若忽略 AbortSignal，会增加取消延迟但不应绕过最终 drain。
- [OPEN] 外部进程强杀与可观测一致性需 process manager 协议补足。

## 严格 60 分钟

- 0–5：画竞态；5–30：两组局部行段精读；30–40：运行 `practice.ts` 状态机预检；40–55：在固定 checkout 找到 wake-latch 相关 spec，运行定向 `pnpm exec vitest run <spec> -t "wake"`；55–60：保存命令和竞态时序。

## 验收

`practice.ts` 的 idle/running/disposed/cancel 预检通过；真实 checkout 的定向 spec 命令与输出已保存；时序图能对应 L104–180 与 L194–311。

## 可选延伸

阅读仓库 cancellation decisions 文档固定提交，不计时。
