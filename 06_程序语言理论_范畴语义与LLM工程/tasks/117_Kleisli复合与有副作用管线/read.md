# 第 117 晚：Kleisli 复合与有副作用管线

## 学习目标

- 由 `η` 和 `bind` 定义 Kleisli 箭头与复合。
- 把 Monad 三律翻译成 Kleisli 范畴的单位、结合律。

## 前置知识与关联任务

需要 116 的 Monad 定义和 106 的范畴定律。

## 必读材料（计入今晚 60 分钟）

| 分钟 | 材料 | 版本 | 精确范围 | 带着什么问题读 |
|---:|---|---|---|---|
| 13 | [Riehl, Category Theory in Context](https://emilyriehl.github.io/files/context.pdf) | author PDF | §5.2 “Kleisli category”，定义至 composition 验证 | Kleisli 箭头为何是 `A→TB` 而非 `TA→TB`？ |
| 7 | [Moggi, Notions of Computation and Monads](https://person.dibris.unige.it/moggi-eugenio/ftp/ic91.pdf) | Information and Computation 93(1), 1991 | PDF pp.2–3：Example 1.1、Definitions 1.2–1.3（Kleisli triple/category） | 值与计算的类型边界怎样进入组合？Kleisli 复合为何等于先运行前一计算再扩张后一函数？ |

## 精读导引

普通函数 `A→B` 的下一步可直接接收 `B`；有失败或状态的函数返回 `T B`，因此复合需要 `bind` 解开一层计算上下文。恒等 Kleisli 箭头是 `η`。不要把 `map` 当成 `bind`：前者不能让回调本身产生新 effect。

## 必须完成的推导或证明

展开 `h >=> (g >=> f)` 与 `(h >=> g) >=> f`，用 Monad 结合律对齐；再指出左右恒等对应哪两条单位律。

## 代码实战

实现 `Result` 的 Kleisli 复合，组合解析、校验和倒数；测试成功、短路失败和结合律。

## 与 DeepSeek Harness / LLM 工业应用的联系

工具流水线中的校验、批准和执行都可能失败；Kleisli 提供“失败保持短路且组合有结合律”的参考语义。Harness 实际使用事件/waterfall 和显式错误协议。

## 60 分钟安排

- 0–5：写 Monad 三律。
- 5–25：精读 Kleisli。
- 25–46：运行 Result 管线。
- 46–55：完成结合律展开。
- 55–60：验收。

## 验收标准

- 正确写出 Kleisli 箭头与复合类型。
- 三类测试及结合律通过。
- 能解释 map 与 bind 的差别。

## 可选延伸

比较 Kleisli triple 与 `η,μ` 表示；不计入今晚。
