# 第179晚：Cordis 论文——统一上下文与观察等价

## 目标与前置

- 目标：理解 unified context、observational equivalence、indistinguishability 与 coeffect-mediated effects。
- 前置：第177–178晚、等价关系、代数操作。

## 计入 60 分钟的必读

| 分钟 | 材料 | 版本 | 精确范围 | 问题 |
|---:|---|---|---|---|
| 33 | [Cordis paper](https://github.com/cordiverse/paper/blob/948a07b369c62adb3b12e102458be5c18dfb69b9/paper.pdf) | 948a07b369c62adb3b12e102458be5c18dfb69b9 | path paper.pdf；§3.3.1–§3.3.3，Definitions 32–41、Lemma 35/38、Theorems 40/42，PDF pp.22–27；checked_at 2026-08-15 | 为什么恢复到观察等价可能比内存逐位相等更合理？ |

## 阅读导引

逐段标出 Γ∞ 将哪些 effect/coeffect 结构统一。为 ≃ 写 reflexive/symmetric/transitive 检查；阅读 Theorem 40 时明确“distinct keys”前提。

## 核心推导

系统只能通过允许的 operations 观察值，因而两个内部状态即使表示不同，只要所有允许观察一致即可视为等价。恢复目标从字节相等提升为 ≃，但等价关系必须与操作兼容，否则可被上下文区分。

## 工业联系与事实标签

- [THEOREM] 论文 Theorem 40 证明不同 keys 上的 operations 独立；Theorem 42 对 coeffect-mediated effect 给出组合性质，结论需带原文假设。
- [EMPIRICAL] 该节是语义论证，没有声称观测到性能提升。
- [INFERENCE] 缓存重建后对象 identity 可变，但若 API 行为一致，插件可按观察等价接受恢复。
- [OPEN] LLM 输出本身的随机性使“观察等价”需由任务级可观测量定义。

## 严格 60 分钟

- 0–5：写两种 equality；5–38：逐段精读；38–53：实现观察投影；53–58：构造内部不同但等价的状态；58–60：标注定理前提。

## 验收

等价正例、可区分反例、空观察边界断言；能解释 distinct-key independence。

## 可选延伸

将观察集合替换为操作闭包，不计时。
