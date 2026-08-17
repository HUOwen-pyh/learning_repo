# 第177晚：Cordis 论文——可逆 Effect 形式模型

## 目标与前置

- 目标：掌握 twisted composition、effect context、track/recover、witnessed effect 与 independence。
- 前置：幺半群、函数复合、左逆、LIFO 栈。

## 计入 60 分钟的必读

| 分钟 | 材料 | 版本 | 精确范围 | 问题 |
|---:|---|---|---|---|
| 35 | [Cordis paper](https://github.com/cordiverse/paper/blob/948a07b369c62adb3b12e102458be5c18dfb69b9/paper.pdf) | 948a07b369c62adb3b12e102458be5c18dfb69b9 | path paper.pdf；§3.1.1–§3.1.3，Definitions 1–19、Theorems 4–16 与 Theorem 20、Lemma 18，PDF pp.9–16；checked_at 2026-08-15 | 为什么逆变换的组合顺序与正向顺序相反？ |

## 阅读导引

逐式抄写 twisted composition、track 与 recover 的类型。每个定理只写“前提→结论”，尤其标出 witnessed、uniform inverse、pairwise independence，并把 p.16 的 Theorem 20 纳入 §3.1.3 笔记；禁止删去前提复述结论。

## 核心推导

若 e1 的 forward/inverse 为 (f1,g1)，e2 为 (f2,g2)，顺序执行正向为 f2∘f1，恢复必须为 g1∘g2。这正是 effect journal LIFO。独立性用于允许与其他组件交错后仍恢复，而非宣称所有副作用天然可逆。

## 工业联系与事实标签

- [THEOREM] 论文 Theorem 7 给出满足逆条件时 track 后 recover 的恢复性质；Theorems 15–16 给出 witnessed composition 的恢复结论，须保留原假设。
- [EMPIRICAL] 本节为形式化构造与证明，不是性能实验。
- [INFERENCE] 工具注册 disposer 可成为 witnessed effect；发送邮件通常只能补偿，不能成为精确逆。
- [OPEN] 对不可逆外部世界 effect，论文的系统边界选择决定可声称的恢复范围。

## 严格 60 分钟

- 0–5：复习复合；5–40：逐定义/定理精读；40–54：实现 journal；54–58：交换 undo 顺序制造反例；58–60：写前提清单。

## 验收

能手推两 effect 的逆序；代码验证恢复、错误顺序、空 journal；不把补偿等同数学逆。

## 可选延伸

继续读 Corollary 21，PDF p.17，不计时。
