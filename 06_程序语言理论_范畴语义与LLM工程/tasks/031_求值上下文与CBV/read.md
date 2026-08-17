# 第 031 晚：求值上下文与 call-by-value

## 学习目标

- 用 evaluation context 描述 CBV 的唯一下一步位置。
- 实现先函数、后实参、最后 β 的小步求值器。
- 用反例说明“实参必须是值”的作用。

## 前置任务

- 第 030 晚“β 归约与多步关系”。

## 必读材料（计入今晚 60 分钟）

| 分钟 | 材料 | 版本 | 精确范围 | 带着问题读 |
|---:|---|---|---|---|
| 14 | [Software Foundations — Stlc](https://softwarefoundations.cis.upenn.edu/plf-current/Stlc.html) | PLF current，页面快照 2026-01 | “Operational Semantics” 的 Values 与 ST_AppAbs/ST_App1/ST_App2 | 三条规则为何没有重叠？ |
| 10 | [PLFA — Lambda](https://plfa.github.io/22.08/Lambda/) | 22.08 | “Reduction” 中 `ξ-·₁`、`ξ-·₂`、`β-ƛ` 规则及第一个 sequence | 哪条 premise 强制左到右 CBV？ |

## 精读导引

把上下文写成 `E ::= [] | E t | v E`。它是“只有一个洞的 AST”，描述下一步 redex 的位置。对 `((λx.x) ((λy.y) v))` 圈出唯一上下文和 redex。

## 必须完成的推导

1. 由 `E` 文法重建三条 CBV 应用规则。
2. 推导嵌套项的两步轨迹。
3. 说明若同时允许在左右任意归约，确定性证明在哪一 case 失效。

结论类型：【基础定理】给定确定的基本 redex 与唯一上下文分解，CBV 一步关系是确定的。

## 与 DeepSeek Harness / LLM 工业应用的联系

直接联系是调度次序：工具调用前先把工具名/参数求成可执行值，类似 CBV 的阶段约束。明确 evaluation context 能避免同一状态出现多个隐式调度解释。

## 60 分钟安排

| 环节 | 分钟 |
|---|---:|
| 必读材料 | 24 |
| 上下文分解推导 | 11 |
| 完成 CBV step/trace | 20 |
| 验收 | 5 |
| **合计** | **60** |

## 验收标准

- 能从 `E` 文法说出求值顺序。
- 每个非值测试项最多有一个下一步。
- 正例、自由变量 stuck 反例、已是值边界例通过。

## 可选延伸

- 实现 `decompose(t) -> (context, redex)` 与 `plug` 往返。

