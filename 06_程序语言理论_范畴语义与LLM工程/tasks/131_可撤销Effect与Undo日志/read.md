# 第 131 晚：可撤销 Effect 与 Undo 日志

## 学习目标

- 区分数学可逆函数、补偿动作与 Cordis 跟踪的可撤销注册。
- 用 LIFO disposer journal 恢复插件挂载前状态。

## 前置知识与关联任务

回顾 013 的群/逆、088 的 undo log 和 125 的 handler。

## 必读材料（计入今晚 60 分钟）

| 分钟 | 材料 | 版本 | 精确范围 | 带着什么问题读 |
|---:|---|---|---|---|
| 10 | [Cordis Primer](https://github.com/deepseek-ai/deepseek-harness/blob/47f943859bef60e4160492346772ded9b24f765a/docs/cordis-primer.md) | commit `47f943…` | “Registrations are reversible effects”与 Practical Rules 最后一段 | disposer 为什么必须与注册由同一生命周期拥有？ |
| 10 | [DeepSeek Harness architecture](https://github.com/deepseek-ai/deepseek-harness/blob/47f943859bef60e4160492346772ded9b24f765a/docs/architecture.md) | `47f943…` | Cordis 段落，特别是 registrations unwind on unload | 卸载要恢复哪些可观察状态？ |

## 精读导引

注册 listener 后返回 disposer 是可撤销注册；这不意味着网络请求、文件写入等任意 effect 都有数学逆。多个注册通常按栈逆序撤销，以免先删底层服务后再撤上层依赖。课程把 group/逆半群用于进一步建模时标记为 INFERENCE。

## 必须完成的推导或证明

给 `service→listener→tool` 三次注册写出唯一安全的撤销顺序，并构造正序撤销访问已删除服务的反例。

## 代码实战

实现 disposer journal；异常发生在第 k 次注册时也必须撤销此前所有注册并恢复快照。

## 与 DeepSeek Harness / LLM 工业应用的联系

这是 Cordis temporal composability 的直接工程核心（FACT）。HMR、配置变化和插件卸载都依赖无残留清理。

## 60 分钟安排

- 0–5：区分 inverse/compensation/disposer。
- 5–25：精读固定文档。
- 25–46：实现 undo journal。
- 46–55：故障注入和顺序证明。
- 55–60：验收。

## 验收标准

- 正常卸载与中途失败都恢复原状态。
- 明确 LIFO 必要性。
- 不声称任意外部副作用可逆。

## 可选延伸

阅读固定 Cordis `fiber.ts`；不计入今晚。
