# 第 053 晚：System F：显式类型抽象与 Church 编码

## 具体目标

- 表示 `∀α.A`、类型抽象 `Λα.e` 和类型应用 `e [B]`。
- 实现避免变量捕获的类型替换。
- 检查 polymorphic identity 在 Bool 和 Nat 上的实例。

## 前置编号

- 必须完成：051–052
- 开始前应能回答：HM 的隐式量化与 System F 的显式 `Λ`/类型应用有何区别？

## 必读（20 分钟，计入本晚 60 分钟）

| 分钟 | 材料与版本 | 精确章节、页码或页内标题 | 带着什么问题读 |
|---:|---|---|---|
| 5–15 | [Krishnaswami, Cambridge Types Lecture 5（讲义 PDF 直链）](https://www.cl.cam.ac.uk/teaching/2425/Types/lec-5-handout.pdf) | PDF pp. 2–5（页脚 1–4）：System F 语法、类型良构与 typing rules | 类型抽象引入规则为什么要求类型变量不被环境约束？ |
| 15–25 | [Krishnaswami, Cambridge Types Lecture 5（讲义 PDF 直链）](https://www.cl.cam.ac.uk/teaching/2425/Types/lec-5-handout.pdf) | PDF pp. 17–19（页脚 16–18）：Church encodings、Boolean 编码与条件求值 | 把类型当作参数后，Boolean 的数据选择如何化成类型应用与函数应用？ |

以上链接直接指向教材作者、大学课程或原始论文；阅读只到表中边界，不顺延挤占实战时间。

## 导读

System F 把多态选择公开成语法，因此检查器不再猜量化位置。`Λα.e` 产生全称类型，类型应用执行类型层替换；这一显式性适合学习 parametricity，也揭示 HM 推断隐藏了什么。

## 今晚必须完成的推导或证明

完整推导 `Λα. λx:α. x : ∀α. α→α`，再推导其在 `Bool` 上的类型应用。指出每次规则引入或消去的 binder。

把推导写在纸上或个人笔记中；关键规则名、每一步产生的约束以及失败位置必须可复查，不能只记录最终答案。

## 与 DeepSeek Harness / LLM 工程的联系

参数化插件接口承诺实现不能窥探调用者选择的类型。虽然 TypeScript 泛型不是 System F 的完整实现，parametricity 仍是判断通用服务 API 是否泄漏具体实现的好工具。

这里的联系是工程建模用途，不声称 Harness 直接实现了本节全部形式系统。

## 严格 60 分钟

| 时间 | 动作 | 到点产物 |
|---:|---|---|
| 0–5 | 闭卷回忆前置概念并写一个例子 | 一条定义和一个反例 |
| 5–25 | 完成上表两段必读 | 两个阅读问题的短答 |
| 25–38 | 完成指定推导/证明 | 可逐步检查的推导 |
| 38–55 | 阅读并运行 `practice.py`，完成动手改造 | 全部断言通过 |
| 55–60 | 对照验收清单，写下一个未解决问题 | 验收记录 |

总计严格为 60 分钟；可选延伸不属于今晚预算。

## 验收

- [ ] 能区分 term binder 与 type binder。
- [ ] 脚本覆盖合法实例化、错误 term application、类型变量 shadowing 边界。
- [ ] 动手改造：编码 Church Boolean 的 System F 类型。

## 可选延伸（不计入 60 分钟）

阅读 Cambridge Lecture 5 的 Church numeral，写出 `zero` 和 `succ` 的类型。
