# 第 047 晚：引用类型、store typing 与保持性

## 学习目标

- 用 `Σ` 将 location 映射到其固定 cell 类型。
- 定义 concrete store 与 store typing 一致。
- 理解分配为何要求扩展 `Σ` 版本的 preservation。

## 前置任务

- 第 046 晚“位置、store 与带状态的小步语义”。

## 必读材料（计入今晚 60 分钟）

| 分钟 | 材料 | 版本 | 精确范围 | 带着问题读 |
|---:|---|---|---|---|
| 15 | [Software Foundations — References](https://softwarefoundations.cis.upenn.edu/plf-current/References.html) | PLF current，页面快照 2026-01 | store typing 动机：从直接按 store 内容定 loc 类型，到 `store_ty`/T_Loc | 为什么循环 store 迫使类型与具体值解耦？ |
| 13 | [Software Foundations — References](https://softwarefoundations.cis.upenn.edu/plf-current/References.html) | PLF current，页面快照 2026-01 | “The Typing Relation” 的 T_Loc/T_Ref/T_Deref/T_Assign；“Well-Typed Stores” 定义 | 赋值为何必须保持 cell 的初始类型？ |

## 精读导引

`Σ[i]=T` 是 location i 的稳定承诺，不是每次读取当前值再猜类型。well-typed store 要求长度相等且每个值符合对应 T。分配使 store 与 Σ 同步增长，因此 preservation 结论允许 `Σ′` 扩展 `Σ`。

## 必须完成的推导

1. 写 T_Loc/T_Ref/T_Deref/T_Assign。
2. 说明 `ref true` 从空 Σ 归约到 `loc 0` 时，旧 Σ 为什么不够。
3. 写出 store well-typed 的逐 location 条件。

结论类型：【状态保持性】归约后存在扩展 Σ′，使新项同类型且新 store 与 Σ′ 一致。

## 与 DeepSeek Harness / LLM 工业应用的联系

直接联系：外部资源 ID 也需要独立的类型/权限目录；不能每次根据当前 payload 猜契约。创建资源时目录扩展，更新时则必须维持既定 schema。

## 60 分钟安排

| 环节 | 分钟 |
|---|---:|
| 必读材料 | 28 |
| 四规则与分配 case | 12 |
| 完成 typed store | 16 |
| 验收 | 4 |
| **合计** | **60** |

## 验收标准

- concrete store 与 Σ 长度、逐 cell 类型一致。
- 同类型赋值成功，异类型赋值被拒绝。
- 空 store 分配边界正确扩展 Σ。

## 可选延伸

- 实现 `extends(old,new)` 并检查旧 location lookup 在扩展后不变。

