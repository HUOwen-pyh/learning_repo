# 第 112 晚：幺半范畴与张量组合

## 学习目标

- 区分普通范畴复合与张量 `⊗` 表示的并列组合。
- 写出结合子、左右单位子和 coherence 的作用。

## 前置知识与关联任务

回顾 015–021 的幺半群、106 的函子和 108 的自然变换。

## 必读材料（计入今晚 60 分钟）

| 分钟 | 材料 | 版本 | 精确范围 | 带着什么问题读 |
|---:|---|---|---|---|
| 14 | [Fong & Spivak, Seven Sketches（作者 PDF）](https://dspivak.net/7Sketches.pdf) | author PDF | §4.4.3，书页 136–138（PDF pp. 147–149）：Rough Definition 4.45 至 Example 4.49 | `⊗` 作为函子时，如何同时作用于对象和态射？ |
| 6 | [Fong & Spivak, Seven Sketches（作者 PDF）](https://dspivak.net/7Sketches.pdf) | author PDF | §4.4.3，书页 137（PDF p. 148）：Remark 4.46–4.47，strictness 与 Mac Lane coherence | coherence 为什么允许 wiring diagram 省略结合子与单位子？ |

## 精读导引

范畴复合是串行连接，张量是并列连接；二者通过函子性相容。Python 二元组给出 `Set` 中笛卡尔幺半结构，但并非所有张量都有复制或丢弃。Monad 的“幺半群对象”说法以后依赖这一层，今晚先把对象级结合、单位和结构同构分清。

## 必须完成的推导或证明

写出 `(A⊗B)⊗C → A⊗(B⊗C)` 的 associator 及逆；用具体三元组验证两边单位子。

## 代码实战

实现嵌套元组的 associator/unitors，检查往返和一个简化 coherence 路径；坏 associator 会丢值并被反例捕获。

## 与 DeepSeek Harness / LLM 工业应用的联系

工具的串行依赖与无依赖并发是两种不同组合。幺半范畴提供表达并列组合的语言，但实际并发还需处理取消、资源和时序（INFERENCE）。

## 60 分钟安排

- 0–5：写幺半群三条律。
- 5–25：精读幺半范畴。
- 25–45：运行 associator/unitors 实验。
- 45–55：画串行与并列组合图。
- 55–60：阶段验收。

## 验收标准

- 不混淆 `∘` 与 `⊗`。
- associator 两向往返及单位测试通过。
- 能解释为何“严格相等”可被 coherence 安全弱化。

## 可选延伸

阅读 braided/symmetric monoidal category；不计入今晚。
