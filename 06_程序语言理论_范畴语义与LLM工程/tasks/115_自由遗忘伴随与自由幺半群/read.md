# 第 115 晚：自由—遗忘伴随与自由幺半群

## 学习目标

- 证明列表/词构造是集合到幺半群的自由函子。
- 将任意生成元函数唯一延拓为幺半群同态。

## 前置知识与关联任务

回顾 015–021 的幺半群、自由幺半群和同态，以及 113 的伴随。

## 必读材料（计入今晚 60 分钟）

| 分钟 | 材料 | 版本 | 精确范围 | 带着什么问题读 |
|---:|---|---|---|---|
| 12 | [Riehl, Category Theory in Context](https://emilyriehl.github.io/files/context.pdf) | author PDF | §4.1 的 free-forgetful adjunction 示例 | 唯一延拓为什么就是 fold？ |
| 8 | [Cambridge CAT notes](https://www.cl.cam.ac.uk/teaching/2324/CAT/CATLectureNotes.pdf) | 2023–24 | Lecture 3 “Free monoids”定义及泛性质 | 生成元嵌入 `η_X` 的角色是什么？ |

## 精读导引

`Free(X)` 的元素是有限词，乘法是拼接，单位是空词。给集合函数 `f:X→U(M)`，唯一幺半群同态 `f*:Free(X)→M` 逐词 fold。存在性靠 fold 构造；唯一性靠任意同态必须保持空词和拼接，再对词长归纳。

## 必须完成的推导或证明

对词长做归纳，证明任何延拓 `h` 必等于 `fold(f)`；同时验证 `h([])=e`、`h(u++v)=h(u)·h(v)`。

## 代码实战

实现通用自由幺半群 fold，在字符串拼接和整数加法两个目标幺半群上验证同态律，并提供错误单位反例。

## 与 DeepSeek Harness / LLM 工业应用的联系

append-only event 序列天然有自由幺半群结构；把事件 fold 成 projection 是同态候选。只有 fold 尊重拼接时，分段 replay 才与整段 replay 一致（INFERENCE，之后对真实 log 验证）。

## 60 分钟安排

- 0–5：写幺半群律。
- 5–25：精读自由泛性质。
- 25–45：运行两个目标幺半群实验。
- 45–55：完成唯一性归纳。
- 55–60：验收。

## 验收标准

- 能写出伴随 Hom 双射的两侧。
- fold 同态律和错误单位反例通过。
- 唯一性证明明确使用词长归纳。

## 可选延伸

构造自由群并比较约简；不计入今晚。
