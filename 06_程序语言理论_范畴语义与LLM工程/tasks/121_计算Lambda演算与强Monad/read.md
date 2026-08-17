# 第 121 晚：计算 Lambda 演算与 strong Monad

## 学习目标

- 说明 strength `A×TB→T(A×B)` 如何让纯环境与 effectful 计算交互。
- 识别一般 Monad 与可解释计算 lambda calculus 所需附加结构。

## 前置知识与关联任务

需要 112 的幺半/笛卡尔结构、116 的 Monad 和 120 的值/计算区分。

## 必读材料（计入今晚 60 分钟）

| 分钟 | 材料 | 版本 | 精确范围 | 带着什么问题读 |
|---:|---|---|---|---|
| 20 | [Moggi, Computational Lambda-Calculus and Monads](https://person.dibris.unige.it/moggi-eugenio/ftp/lc88.pdf) | LICS 1989 作者直链版本 | PDF 第 2–3 页：Example 2.1 从 `let` 的类型缺口读到 `t_{A,B}: A×TB→T(A×B)`；Definition 2.2 的 strong monad 定义及紧随其后的四条相容式；Remark 2.3 前两段对四条式子的解释 | 为什么普通 monad 加笛卡尔积仍不足？四条式子分别怎样约束终对象、结合子、`η` 与 `μ`？ |

## 精读导引

不要先背定义；先复算 Example 2.1 的类型缺口：`⟨id,g₂⟩` 的余域是 `A×TB`，但 Kleisli extension 要接收 `T(A×B)`，中间正缺 strength。随后把 Definition 2.2 的四式逐条标成：终对象 coherence、积结合 coherence、与 `η` 相容、与 `μ` 相容。在含积的语义中，函数体既依赖纯环境又执行 effect；strength 允许把未受 effect 的环境带入计算，而不是随意交换 effect 顺序。对 State，`(a, stateful_b)` 运行后产生 `((a,b),s')`，纯 `a` 不改变状态。

## 必须完成的推导或证明

为 State 写出 strength，并验证 `(id×η);t = η` 的单位相容实例；再用“先展平嵌套 State、后 strength”和“先 strength、再两层映射并展平”得到相同结果，解释这是 Definition 2.2 的 `μ` 相容式。说明若 strength 重复运行计算会破坏哪条观察性质。

## 代码实战

实现 State strength，检查纯环境保持、状态只更新一次和自然性有限实例；坏实现运行两次必须失败。

## 与 DeepSeek Harness / LLM 工业应用的联系

工具执行需要携带纯元数据、策略上下文和实际副作用。strength 提供组合思路，但 Harness 依靠显式 runtime context、事件和权限流水线，而非直接暴露该抽象。

## 60 分钟安排

- 0–5：写 strength 类型。
- 5–25：精读定义和图表。
- 25–46：运行 State strength。
- 46–55：完成相容性推导和坏例。
- 55–60：验收。

## 验收标准

- strength 类型和 effect 顺序正确。
- 状态只更新一次的断言通过。
- 能说明额外结构为何必要。

## 可选延伸

研究 commutative monads；不计入今晚。
