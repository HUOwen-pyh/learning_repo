# 第170晚：Cordis 教程 2——生命周期与 Effect

## 目标与前置

- 目标：掌握 fiber 状态机、ctx.effect 与自动清理。
- 前置：第169晚、资源获取即初始化、Promise。

## 计入 60 分钟的必读

| 分钟 | 材料 | 版本 | 精确范围 | 问题 |
|---:|---|---|---|---|
| 20 | [Lifecycle and effects](https://github.com/deepseek-ai/deepseek-harness/blob/47f943859bef60e4160492346772ded9b24f765a/docs/cordis-tutorial/02-lifecycle-and-effects.md#L1-L98) | Harness 47f943859bef60e4160492346772ded9b24f765a | path docs/cordis-tutorial/02-lifecycle-and-effects.md；全章 L1–L98；symbols ctx.effect、fiber.dispose、FiberState；checked_at 2026-08-15 | 哪些注册已经是 effect？异步 disposer 如何排序？ |

## 阅读导引

画 PENDING→LOADING→ACTIVE→UNLOADING→DISPOSED 与 FAILED。区分“disposer 逆注册顺序启动”和“多个 async disposer 并发”这两个事实。

## 核心推导

effect acquire 返回 release，fiber 记录 release。卸载将 effect journal 逆序展开；若 acquire 失败，则只清理此前成功获取的资源。幂等 dispose 防止重复释放。

## 工业联系与事实标签

- [THEOREM] 对严格 LIFO 且每个 release 为 acquire 的左逆，完整 unwind 恢复初始资源状态。
- [EMPIRICAL] 固定教程明确 Cordis 异步 disposers 可并发；强制顺序需放在同一 disposer 内 await。
- [INFERENCE] 工具注册、监听器与子插件统一成 effect 可显著降低热重载泄漏。
- [OPEN] 外部不可逆动作无法由 disposer 真正撤销，只能补偿。

## 真实固定 checkout 实战

继续使用第 169 晚的同一 `tmp/cordis-tutorial`。按官方第二章创建 `lifecycle.ts`，把 `cordis.yml` 指向它，并运行真实 launcher。证据必须显示 `heartbeat plugin loading`、至少一次 `tick`、`heartbeat cleaned up`、最后的 `disposed`，且进程正常退出；这些行共同证明 effect 确实由真实 fiber 获取并在 `await fiber.dispose()` 后清理，而不只是本地 journal 的模拟结果。

## 严格 60 分钟

- 0–5：闭卷画 fiber 状态机并标出失败分支。
- 5–25：精读固定提交第二章 L1–L98。
- 25–37：运行本地 `practice.ts`，检查逆序、幂等 dispose 与加载失败回滚。
- 37–42：在连续教程工作区按章创建 `lifecycle.ts` 并更新 `cordis.yml`。
- 42–52：运行 `node --import tsx ../../vendor/cordis/bin.js`，保存完整生命周期输出与退出码。
- 52–55：核对清理发生在 `disposed` 之前，且进程没有残留 timer。
- 55–60：核对双门证据并写三句复盘。

## 验收

- 本地门：逆序、重复 dispose、部分加载失败与回滚断言全部通过，并能解释 async disposer caveat。
- 真实门：固定 HEAD 下的官方 launcher 退出 0；输出同时含加载、tick、`heartbeat cleaned up` 和 `disposed`，退出后无继续 tick。
- 两门必须同时通过；真实 fiber 的清理输出不能由 `practice.ts` 的日志替代。

## 可选延伸

阅读 vendor/cordis/src/fiber.ts，留到第177晚源码对应。
