# 第168晚：类型化事件总线与工具注册验收

## 目标与前置

- 目标：组合事件表、泛型总线、工具参数表与运行时 validator，形成插件骨架。
- 前置：第162–167晚。

## 计入 60 分钟的必读

| 分钟 | 材料 | 版本 | 精确范围 | 问题 |
|---:|---|---|---|---|
| 8 | [TypeScript Generics](https://www.typescriptlang.org/docs/handbook/2/generics.html) | checked_at 2026-08-15 | Generic Constraints | 事件名与 payload 如何保持相关？ |
| 7 | [TypeScript Narrowing](https://www.typescriptlang.org/docs/handbook/2/narrowing.html#using-type-predicates) | checked_at 2026-08-15 | User-defined type guards | validator 怎样把 unknown 缩窄？ |
| 5 | [DSPy paper](https://proceedings.iclr.cc/paper_files/paper/2024/file/f1cf02ce09757f57c3b93c0db83181e0-Paper-Conference.pdf) | ICLR 2024 | §3 Programming model 回顾 | IR 契约怎样连接运行时？ |

## 阅读导引

编译期用 EventMap/ToolMap 保持键值关系；边界输入始终为 unknown，先 validator 后 handler。不要用 as 断言跳过验证。

## 核心推导

emit<K extends keyof E>(k:K,p:E[K]) 在编译期关联名称与 payload。工具 call 接收 unknown，validator 是从 unknown 到 A 的部分证明；仅成功分支可调用 handler(A)。

## 工业联系与事实标签

- [THEOREM] 泛型签名可在编译期排除已声明事件名与 payload 类型的不匹配。
- [EMPIRICAL] JavaScript 运行时不会执行 TypeScript 类型，边界验证不可省略。
- [INFERENCE] 同一契约可生成 schema、文档和测试夹具，降低漂移。
- [OPEN] 类型级 schema 与完整 JSON Schema 语义的一致生成仍受库和语言表达力限制。

## 严格 60 分钟

- 0–5：画契约；5–25：必读；25–50：运行总线和工具；50–57：新增 divide 并验证零除；57–60：周验收。

## 验收

事件顺序、非法参数、零监听边界断言；无第三方 import；能指出 runtime boundary。

## 可选延伸

加入异步 handler 与错误聚合策略，不计时。
