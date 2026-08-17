# 第 026 晚：捕获规避替换

## 学习目标

- 按定义实现 `t[x:=s]`。
- 识别 binder 捕获自由变量的危险分支。
- 用 α 改名和新鲜名修复捕获。

## 前置任务

- 第 024 晚“绑定、自由变量与遮蔽”。
- 第 025 晚“α 等价与名字规范化”。

## 必读材料（计入今晚 60 分钟）

| 分钟 | 材料 | 版本 | 精确范围 | 带着问题读 |
|---:|---|---|---|---|
| 18 | [PLFA — Lambda](https://plfa.github.io/22.08/Lambda/) | 22.08 | “Substitution” 全节，重点读 capture example 与 `subst` 定义 | 进入 `λy.t` 前为何要检查 `y∈FV(s)`？ |
| 7 | [Software Foundations — Stlc](https://softwarefoundations.cis.upenn.edu/plf-current/Stlc.html) | PLF current，页面快照 2026-01 | “Operational Semantics” → “Substitution” 至 examples 结束 | substitution 为何只替换自由出现？ |

## 精读导引

逐分支处理变量、应用、抽象。抽象有三种情况：binder 就是目标变量、binder 与替入项无冲突、binder 会捕获替入项自由变量。第三种必须先 α 改名；为使实现直接可靠，新名字应避开 body 中全部名字（包括内层 binder）以及替入项自由变量，否则可能被同名内层 binder 再次捕获。

## 必须完成的推导

1. 完整写出三构造器的替换递推定义。
2. 手算 `(λy.x)[x:=y]`，结果必须 α 等价于 `λz.y`，不能是 `λy.y`。
3. 说明 `(λx.t)[x:=s]=λx.t` 的遮蔽分支。

结论类型：【基础定义】捕获规避是 substitution 的语义条件，不是美化变量名。

## 与 DeepSeek Harness / LLM 工业应用的联系

这是基础但可迁移的联系：模板实例化、宏展开、prompt 变量注入若忽略作用域，也会发生“用户值被局部名字误绑定”。今晚的算法提供可测试的卫生替换模型。

## 60 分钟安排

| 环节 | 分钟 |
|---|---:|
| 必读材料 | 25 |
| 三分支推导 | 12 |
| 完成 `practice.py` | 19 |
| 验收 | 4 |
| **合计** | **60** |

## 验收标准

- 能当场指出朴素替换的捕获错例。
- 替换算法只更改目标变量的自由出现。
- 正例、遮蔽反例、需改名边界例全部通过。

## 可选延伸

- 添加 property test：替换结果的自由变量是 `(FV(t)-{x})∪FV(s)` 的子集。
