# 第 111 晚：极限、余极限与一致性约束

## 学习目标

- 用锥、余锥和终/始泛性质定义极限与余极限。
- 把积、等化子和 pullback 识别为极限的特例。

## 前置知识与关联任务

回顾 100–103 的积、余积和始末对象，以及 108 的自然性图表。

## 必读材料（计入今晚 60 分钟）

| 分钟 | 材料 | 版本 | 精确范围 | 带着什么问题读 |
|---:|---|---|---|---|
| 14 | [Riehl, Category Theory in Context](https://emilyriehl.github.io/files/context.pdf) | author PDF | §3.1，书页 82–85（PDF pp. 101–104）：Definitions 3.1.1–3.1.8，cone、limit 与 colimit | “兼容锥”要求哪些三角形交换？ |
| 6 | 同书 | author PDF | §3.1，书页 88–89（PDF pp. 107–108）：Definition 3.1.23 的 coproduct、initial object、coequalizer 与 pushout | 对偶后终对象为何变成始对象？ |

## 精读导引

图式描述多个对象与约束，锥给一个候选统一视图；极限是所有兼容视图中的终对象。`Set` 中 pullback 是满足相等约束的配对集合。余极限反向粘合数据。不要把任意收集数据的对象叫极限，必须验证唯一中介态射。

## 必须完成的推导或证明

把二对象离散图式的极限化简为积；把一对平行箭头图式的极限化简为等化子。

## 代码实战

计算两个有限映射的 pullback，检查每个结果满足一致性条件，并验证一个锥唯一分解。

## 与 DeepSeek Harness / LLM 工业应用的联系

把多个 provider 的兼容配置合并成一致视图可以用极限作抽象模型；实际 Harness patch 是有顺序的整行替换，不能未经证明就称为范畴极限（INFERENCE 边界）。

## 60 分钟安排

- 0–5：画积作为锥。
- 5–25：精读 cone/limit/colimit。
- 25–45：运行 pullback 实验。
- 45–55：完成两个特例推导。
- 55–60：验收。

## 验收标准

- 能给出锥和极限的泛性质。
- pullback 的一致性与唯一中介测试通过。
- 能明确区分数学模型和 Harness 现行 patch 语义。

## 可选延伸

阅读 filtered colimits；不计入今晚。
