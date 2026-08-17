# 第 113 晚：伴随的 Hom 集自然双射

## 学习目标

- 以 `Hom_D(Fc,d) ≅ Hom_C(c,Gd)` 的自然双射定义伴随。
- 从类型判断左右函子、单位和余单位的方向。

## 前置知识与关联任务

需要 106 的函子、108 的自然性和 110 的 Hom 函子。

## 必读材料（计入今晚 60 分钟）

| 分钟 | 材料 | 版本 | 精确范围 | 带着什么问题读 |
|---:|---|---|---|---|
| 14 | [Riehl, Category Theory in Context](https://emilyriehl.github.io/files/context.pdf) | author PDF | §4.1，从 Definition 4.1.1 至首个 free/forgetful 例 | 双射要对哪两个变量自然？ |
| 6 | [Cambridge CAT notes](https://www.cl.cam.ac.uk/teaching/2324/CAT/CATLectureNotes.pdf) | 2023–24 | Lecture 12 的 adjunction 定义框 | 为什么只给同样大小的 Hom 集不够？ |

## 精读导引

先把 `F:C→D`、`G:D→C` 的类型写在页顶。转置把 `Fc→d` 变成 `c→Gd`，逆转置反向。双射必须随 `c,d` 的态射自然变化；某次偶然的集合等势不是伴随。用 curry/uncurry 回忆 `(-×A) ⊣ (-)^A`。

## 必须完成的推导或证明

对笛卡尔闭范畴写出 `Hom(X×A,B)≅Hom(X,B^A)`，验证两方向就是 102 的 curry/uncurry βη。

## 代码实战

在有限函数表上检查 curry/uncurry 双射，并验证 pre/post-compose 后转置结果一致的自然性实例。

## 与 DeepSeek Harness / LLM 工业应用的联系

伴随常表达“自由生成语法”与“忘掉结构”间的最优转换。它帮助理解从声明生成运行时结构的关系，但具体 Typert/配置生成器是否形成伴随需另证（INFERENCE）。

## 60 分钟安排

- 0–5：写函子方向。
- 5–25：精读伴随定义。
- 25–45：运行双射实验。
- 45–55：完成指数伴随推导。
- 55–60：验收。

## 验收标准

- 正确写出 Hom 双射和自然性变量。
- curry/uncurry 往返及自然性实例通过。
- 能指出“等势但不自然”的缺陷。

## 可选延伸

阅读 Riehl 的 adjunction of two variables；不计入今晚。
