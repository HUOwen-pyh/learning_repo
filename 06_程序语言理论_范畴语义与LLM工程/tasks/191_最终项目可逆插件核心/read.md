# 第191晚：最终项目——可逆插件核心

## 目标与前置

- 目标：实现 fiber-owned effect journal、服务依赖激活与幂等卸载。
- 前置：第170、171、177晚。

## 计入 60 分钟的必读

| 分钟 | 材料 | 版本 | 精确范围 | 问题 |
|---:|---|---|---|---|
| 12 | [Cordis lifecycle tutorial](https://github.com/deepseek-ai/deepseek-harness/blob/47f943859bef60e4160492346772ded9b24f765a/docs/cordis-tutorial/02-lifecycle-and-effects.md#L1-L88) | Harness 47f943859bef60e4160492346772ded9b24f765a | path docs/cordis-tutorial/02-lifecycle-and-effects.md；L1–88（文件末尾）；symbols ctx.effect/fiber.dispose；checked_at 2026-08-15 | 哪些 release 必须归同一 fiber？ |
| 8 | [Cordis services tutorial](https://github.com/deepseek-ai/deepseek-harness/blob/47f943859bef60e4160492346772ded9b24f765a/docs/cordis-tutorial/03-services.md#L1-L86) | 同一 commit | path docs/cordis-tutorial/03-services.md；L1–86（文件末尾）；symbols Service/inject；checked_at 2026-08-15 | 服务撤销怎样传播？ |

## 阅读导引

把 registry change 本身也写成 effect。加载中任一 acquire 抛错时，只展开已成功项；dispose 多次不得重复 release。

## 核心推导

Fiber 持有 journal，而非全局 disposer 数组，因此所有权可局部推断。inject 条件决定何时建立 journal；依赖消失触发整本 journal 逆序展开。

## 工业联系与事实标签

- [THEOREM] 每项 disposer 恰执行一次且逆序时，有限 journal 的 dispose 终止并清空。
- [EMPIRICAL] Harness 教程称 Cordis registration APIs 已作为 effects 管理。
- [INFERENCE] 插件卸载泄漏应作为测试失败而非仅日志警告。
- [OPEN] 不可逆外部操作需补偿语义。

## 严格 60 分钟

- 0–5：核对固定 SHA；5–25：必读；25–35：运行 `practice.ts` 的 LIFO/失败事务预检；35–55：在真实 capstone package 用 Cordis `ctx.effect` 和 service/inject 写 mount、unload、第二项 acquire 失败回滚的定向 spec；55–60：保存 diff 与 Vitest 输出。

## 验收

预检含 LIFO、幂等、失败 rollback、空 fiber；真实 checkout 的 Cordis spec 证明卸载与部分 acquire 失败均无残留，并保存 SHA、diff、命令和输出。

## 可选延伸

支持 async disposer 和错误聚合，不计时。
