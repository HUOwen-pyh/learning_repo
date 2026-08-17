# 第 102 晚：指数对象与函数类型

## 学习目标

- 用 evaluation 态射和 currying 的泛性质定义指数对象。
- 将函数引入/消去规则对应到 curry 与 eval。

## 前置知识与关联任务

需要 100 的积、036–042 的函数类型和 099 的判断解释。

## 必读材料（计入今晚 60 分钟）

| 分钟 | 材料 | 版本 | 精确范围 | 带着什么问题读 |
|---:|---|---|---|---|
| 12 | [Cambridge Category Theory lecture notes](https://www.cl.cam.ac.uk/teaching/2324/CAT/CATLectureNotes.pdf) | 2023–24 | Lecture 5 “Exponentials”至 currying bijection | `C(X×A,B) ≅ C(X,B^A)` 两边各表示什么？ |
| 8 | [Awodey, Categorical Logic](https://awodey.github.io/catlog/notes/catlog4.pdf) | draft notes | §4.3 中 implication/exponential | β、η 方程分别来自哪一方向？ |

## 精读导引

不要先把 `B^A` 当作 Python 函数集合；先记住它代表从 `A` 到 `B` 的映射，并带有 `eval:B^A×A→B`。任意带额外环境 `X` 的 `f:X×A→B` 必须唯一 curry 成 `X→B^A`。这正是闭包把环境捕获进函数值的抽象接口。

## 必须完成的推导或证明

从 currying 双射推出 `eval∘(curry(f)×id)=f` 和 `curry(eval∘(g×id))=g`。

## 代码实战

用显式环境实现 curry/uncurry，穷举有限输入检查两方向互逆；加入错误捕获环境的反例。

## 与 DeepSeek Harness / LLM 工业应用的联系

插件回调和 waterfall listener 都是携带环境的函数值。指数对象解释“依赖显式输入的二元过程”如何被重组为“已捕获上下文的一元能力”。

## 60 分钟安排

- 0–5：写函数类型的引入/消去规则。
- 5–25：精读 exponentials。
- 25–46：运行 curry/uncurry 实验。
- 46–55：手推 βη 方程与反例。
- 55–60：验收。

## 验收标准

- 能完整说出指数对象的泛性质。
- 能把 lambda/application 对应到 curry/eval。
- 有限域双向测试通过，坏闭包被检测。

## 可选延伸

比较闭包转换和指数对象；不计入今晚。
