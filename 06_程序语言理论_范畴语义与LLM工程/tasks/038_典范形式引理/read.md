# 第 038 晚：值与典范形式引理

## 学习目标

- 陈述 Bool 与箭头类型的 canonical forms。
- 理解“值 + 类型”如何排除错误外形。
- 写运行时断言模拟反演 lemma。

## 前置任务

- 第 037 晚“算法型类型检查”。

## 必读材料（计入今晚 60 分钟）

| 分钟 | 材料 | 版本 | 精确范围 | 带着问题读 |
|---:|---|---|---|---|
| 15 | [PLFA — Properties](https://plfa.github.io/22.08/Properties/) | 22.08 | “Values do not reduce” 与 `Canonical_⦂_` exercise 的声明/构造器 | 为什么只知道 value 还不足以知道其外形？ |
| 10 | [Software Foundations — Stlc](https://softwarefoundations.cis.upenn.edu/plf-current/Stlc.html) | PLF current，页面快照 2026-01 | “Canonical Forms” 两条 lemma（Bool 与 arrow） | 哪个 premise 提供类型，哪个 premise 提供 value？ |

## 精读导引

典范形式不是“所有 Bool 项都是 true/false”，而是“闭的、良类型、已经是值的 Bool 项”。三项缺一不可。把 lemma 当 typing derivation 的反演：箭头类型的值只能由 T_Abs 对应的 lambda 形成。

## 必须完成的推导

1. 陈述：若 `∅⊢v:Bool` 且 `value v`，则 `v=true` 或 `v=false`。
2. 陈述：若 `∅⊢v:A→B` 且 `value v`，则 `v=λx:A.t`。
3. 指出开放变量为何破坏“不看上下文”的版本。

结论类型：【基础引理】canonical forms 是 progress 证明从“函数值”推进到 β-redex 的桥梁。

## 与 DeepSeek Harness / LLM 工业应用的联系

基础联系：schema 类型与“已验证”状态合用，才能断言对象具有可执行外形。只看 JSON 标签或只看 Python 类名都不足以建立协议安全性。

## 60 分钟安排

| 环节 | 分钟 |
|---|---:|
| 必读材料 | 25 |
| 两条 lemma 与反例 | 13 |
| 完成 canonical 检查 | 17 |
| 验收 | 5 |
| **合计** | **60** |

## 验收标准

- 陈述中明确 closed、typed、value 三条件。
- 函数值/Bool 值各返回唯一外形。
- 错配类型反例与 false 边界例通过。

## 可选延伸

- 为积类型预写 canonical form，供第 043 晚使用。

