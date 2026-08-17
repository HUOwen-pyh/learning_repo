# 第172晚：Cordis 教程 4——类型化事件与 Waterfall

## 目标与前置

- 目标：区分 broadcast、serial、bail、waterfall，并理解事件声明合并。
- 前置：第166、168晚、fold。

## 计入 60 分钟的必读

| 分钟 | 材料 | 版本 | 精确范围 | 问题 |
|---:|---|---|---|---|
| 20 | [Events](https://github.com/deepseek-ai/deepseek-harness/blob/47f943859bef60e4160492346772ded9b24f765a/docs/cordis-tutorial/04-events.md#L1-L100) | Harness 47f943859bef60e4160492346772ded9b24f765a | path docs/cordis-tutorial/04-events.md；章内 Types、Listening、Emitting、Waterfall；L1–L100；symbols ctx.on、emit、waterfall；checked_at 2026-08-15 | waterfall 的返回值怎样进入下一监听器？ |

## 阅读导引

为四种派发写出控制流：是否并发、是否等待、何时停止、返回值怎样累计。注意 ctx.on 本身是 effect，卸载时监听器应消失。

## 核心推导

waterfall 是有序左折叠 x_{i+1}=f_i(x_i)；顺序影响结果。broadcast 适合相互独立观察者；bail 在首个非空结果停止；不要把它们混成一个含糊 emit。

## 工业联系与事实标签

- [THEOREM] 一般函数复合不交换，因此 waterfall 监听器重排会改变结果。
- [EMPIRICAL] 固定提交教程通过 Cordis 事件 API 展示类型声明与自动清理。
- [INFERENCE] prompt 组装适合 waterfall，遥测适合 broadcast。
- [OPEN] 第三方监听器的性能隔离和错误聚合需要明确运行时策略。

## 真实固定 checkout 实战

继续使用同一教程工作区，按官方第四章逐段创建章内指定的事件声明、监听器与发射插件，并让 `cordis.yml` 装载它们。用真实 launcher 分别保留 broadcast 的监听输出和 waterfall 的最终值；然后从配置中移除拥有监听器的插件并重跑同一发射路径，确认该监听输出消失。这里的 declaration augmentation 由仓库 TypeScript 环境检查，卸载语义由真实 `ctx.on` effect 验证，本地事件总线只能作为预检。

## 严格 60 分钟

- 0–5：闭卷写出 waterfall 的左折叠式。
- 5–25：精读固定提交第四章 L1–L100。
- 25–37：运行本地 `practice.ts`，检查顺序、移除与零监听器边界。
- 37–44：在连续教程工作区按章创建事件声明、监听与发射插件并更新配置。
- 44–51：运行真实 launcher，保存 broadcast 输出、waterfall 最终值与退出码。
- 51–55：移除监听器 owner 后重跑，记录同一发射路径不再产生该监听输出。
- 55–60：核对双门证据并写三句复盘。

## 验收

- 本地门：顺序、移除、零监听器断言通过，并能解释 declaration augmentation 只在编译期。
- 真实门：固定 HEAD 下的真实事件输出、waterfall 最终值，以及卸载 listener owner 后输出消失的前后对照齐全。
- 两门必须同时通过；只运行自写 event bus 不算完成 Cordis 事件实战。

## 可选延伸

加入异步 serial 事件，不计时。
