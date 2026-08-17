# 第 059 晚：经典逻辑、控制算子与 CPS

## 具体目标

- 把表达式求值改写成显式 continuation。
- 用 `call/cc` 风格的逃逸 continuation 表达提前结束。
- 比较直接解释与 CPS 解释的可观察结果。

## 前置编号

- 必须完成：057–058
- 闭卷入口问题：CPS 项为什么把“下一步怎么办”显式化为参数？

## 必读（20 分钟，已计入 60 分钟）

| 分钟 | 开放权威一手材料与版本 | 精确章节、页码或页内标题 | 阅读问题 |
|---:|---|---|---|
| 5–15 | [Cambridge Topics in Type Systems 2024–25](https://www.cl.cam.ac.uk/teaching/2425/Types/materials.html) | Lecture 9 “Classical logic” 与 Lecture 10 “Continuation-passing style” 的类型翻译部分 | 双重否定翻译怎样把经典推理嵌入直觉主义系统？ |
| 15–25 | [Plotkin, Call-by-name, call-by-value and the λ-calculus](https://doi.org/10.1016/0304-0208(75)90017-1) | §3–§4 中 call-by-value CPS translation 与模拟结果 | CBV CPS 翻译中 continuation 在什么顺序接收值？ |

只读指定边界；链接均为大学官方讲义、作者版本或正式论文页面。

## 导读

Continuation 可看作当前求值上下文的函数表示。CPS 将控制流数据化，使返回、异常和提前退出可由同一机制表达；逻辑侧对应结论/否定的变换。今晚不把 Python 异常冒充完整 call/cc，而使用显式 continuation。

## 必做推导 / 证明

对 `f (g x)` 写 CBV CPS 翻译，标出 `g`、`f`、最终 continuation 的调用顺序；再写 Peirce law 的经典类型。

必须保留判断形式和规则名；“凭直觉显然”不算完成。

## DeepSeek Harness / LLM 工程联系

Harness 的 waterfall、取消和流式回调都改变“下一步”。CPS 视角帮助审计 continuation 是否恰好调用一次、取消是否绕过了持久化步骤。

这是从形式概念到工程约束的映射；除明确指出外，不宣称 Harness 已静态证明这些性质。

## 严格 60 分钟

| 时间 | 工作 |
|---:|---|
| 0–5 | 回忆入口问题，写定义和反例 |
| 5–25 | 完成必读表并回答两个问题 |
| 25–38 | 手写推导或证明 |
| 38–55 | 运行 `practice.py`，再完成文件顶部的动手改造 |
| 55–60 | 按验收项自测并记录一个疑问 |

5 + 20 + 13 + 17 + 5 = 60 分钟。下面的延伸不得挤入本晚。

## 验收

- [ ] 直接解释与 CPS 解释在普通表达式上相同。
- [ ] 逃逸 continuation 能跳过后续加法。
- [ ] 动手改造：加入错误 continuation，使错误不与正常返回混用。

## 可选延伸（不计时）

阅读 Cambridge Lecture 11 中 continuation applications。

