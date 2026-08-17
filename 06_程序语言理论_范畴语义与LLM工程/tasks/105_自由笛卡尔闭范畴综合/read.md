# 第 105 晚：自由笛卡尔闭范畴综合

## 学习目标

- 把 STLC 语法看成由基本类型生成的自由笛卡尔闭范畴。
- 实现从类型化项到投影、配对、curry、eval 组合子的翻译。

## 前置知识与关联任务

综合 099–104；需要能独立写出变量、配对、投影、lambda、application 的语义。

## 必读材料（计入今晚 60 分钟）

| 分钟 | 材料 | 版本 | 精确范围 | 带着什么问题读 |
|---:|---|---|---|---|
| 13 | [Cambridge Category Theory lecture notes](https://www.cl.cam.ac.uk/teaching/2324/CAT/CATLectureNotes.pdf) | 2023–24 | Lecture 9 “free cartesian closed category”及前后的 soundness/completeness 陈述 | “free”允许什么方程，又禁止凭空加入什么方程？ |
| 7 | [Awodey, Categorical Logic](https://awodey.github.io/catlog/notes/catlog4.pdf) | draft notes | §4.6 的 syntactic category 概览 | 对象和态射的等价类为何要按可证明相等取商？ |

## 精读导引

自由 CCC 的对象由基本类型经 `1,×,⇒` 生成，态射由类型化项在 βη 等价下生成。它既是语法本身的范畴化，也是所有 CCC 模型的初始解释来源。重点理解：任何基本类型解释都唯一延拓为保持 CCC 结构的函子。

## 必须完成的推导或证明

翻译 `λp. (snd p, fst p)`，写出它与自身复合为何等于恒等；指出使用了哪些积 βη 方程。

## 代码实战

脚本实现带类型检查的最小 STLC AST，并把变量、lambda 与 application 翻译为 CCC 的投影、复合、配对、`curry` 与 `eval` 组合子；有限 Bool 语义检查恒等函数、外层变量和函数复合。动手项只需在已有翻译器上加入积类型这一小扩展。

## 与 DeepSeek Harness / LLM 工业应用的联系

这是“接口组合规则决定所有合法实现”的基础范例。后续判断插件组合是否保持契约时，会重复使用这种由生成元与方程定义系统的方法。

## 60 分钟安排

- 0–5：闭卷列出 CCC 生成结构。
- 5–25：精读自由 CCC。
- 25–47：运行翻译器并读组合子树。
- 47–55：完成 swap 证明与错误用例。
- 55–60：阶段验收。

## 验收标准

- 能解释“自由”与“初始解释”的含义。
- STLC→CCC 翻译器的恒等、外层变量、application 与函数复合测试通过。
- 能指出至少一个不由 CCC 方程推出的额外等式。

## 可选延伸

在 AST 中加入积类型、pair 与投影；不计入今晚。
