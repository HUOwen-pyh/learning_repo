# 第 108 晚：自然变换与组件替换

## 学习目标

- 给出自然变换的分量族和自然性方块。
- 区分自然、与元素具体表示无关的转换和偷看元素的偶然转换。

## 前置知识与关联任务

回顾 106–107 的函子。准备画 `F(A)→G(A)` 与 `F(B)→G(B)` 的方块。

## 必读材料（计入今晚 60 分钟）

| 分钟 | 材料 | 版本 | 精确范围 | 带着什么问题读 |
|---:|---|---|---|---|
| 12 | [Riehl, Category Theory in Context](https://emilyriehl.github.io/files/context.pdf) | author PDF | §1.4，从 natural transformation 定义至首个 commuting-square 例 | 分量为什么不能彼此独立选择？ |
| 8 | [Cambridge CAT notes](https://www.cl.cam.ac.uk/teaching/2324/CAT/CATLectureNotes.pdf) | 2023–24 | Lecture 11 “Natural transformations”前半 | 自然性方程的两条路径是什么？ |

## 精读导引

自然变换不是单个函数，而是对每个对象给一个态射，并要求对所有输入态射方块交换。先写类型，再确定方程方向。`head:List A→Option A` 是自然候选，因为重命名元素与取首元素可交换；“若元素恰等于整数 0 就丢弃”不能对所有集合自然定义。

## 必须完成的推导或证明

对 `head` 写出 `Option(f)∘head_A = head_B∘List(f)`，分别验证空表和非空表。

## 代码实战

穷举多个列表和函数检查 `head` 的自然性，并提供依赖具体整数值的坏分量作为反例。

## 与 DeepSeek Harness / LLM 工业应用的联系

替换 provider 时若转换只依赖公开接口而不窥探具体实现，可用自然性作为设计类比。该映射是课程的数学解释（INFERENCE），不是 Harness 的形式证明。

## 60 分钟安排

- 0–5：画空白自然性方块。
- 5–25：精读定义和示例。
- 25–46：运行自然性测试。
- 46–55：完成 `head` 证明和坏分量反例。
- 55–60：验收。

## 验收标准

- 分量、对象和函子的类型全部正确。
- 能口述自然性方程两条路径。
- 好坏转换被可执行测试区分。

## 可选延伸

证明自然变换的竖直复合；不计入今晚。
