# 第 045 晚：记录类型、标签与投影

## 学习目标

- 将二元积推广为带唯一标签的 n 元积。
- 实现 record typing 与按标签 projection。
- 明确字段顺序、唯一性和缺失字段错误。

## 前置任务

- 第 043 晚“积类型、pair 与投影”。

## 必读材料（计入今晚 60 分钟）

| 分钟 | 材料 | 版本 | 精确范围 | 带着问题读 |
|---:|---|---|---|---|
| 18 | [Software Foundations — MoreStlc](https://softwarefoundations.cis.upenn.edu/plf-current/MoreStlc.html) | PLF current，页面快照 2026-01 | “Records” 从开头至 T_Rcd/T_Proj 规则结束 | record 是 pair 的哪两项推广？ |
| 8 | [Software Foundations — MoreStlc](https://softwarefoundations.cis.upenn.edu/plf-current/MoreStlc.html) | PLF current，页面快照 2026-01 | “Records” 中关于重复标签、形式化表示选择的讨论 | 为什么重复 label 会让 projection 不确定？ |

## 精读导引

先把 record type 当 label→type 的有限映射。构造时逐字段 infer；投影时按 label 查类型。运行时 record 只有所有字段均为值才是 value，投影随后返回唯一字段值。

## 必须完成的推导

1. 推导 `{ok=true,msg=false}:{ok:Bool,msg:Bool}`。
2. 推导 `.ok` 的 typing 与一步 reduction。
3. 给出重复标签为何同时破坏静态 lookup 与运行时投影唯一性。

结论类型：【数据建模】label uniqueness 是记录语义的显式 well-formedness 条件。

## 与 DeepSeek Harness / LLM 工业应用的联系

直接联系：工具 schema 和消息对象就是带标签的积；字段唯一、必需字段、投影类型都应在模型输出进入业务代码前验证。今晚暂不允许“额外字段可替代较小记录”，那是第 049 晚。

## 60 分钟安排

| 环节 | 分钟 |
|---|---:|
| 必读材料 | 26 |
| 规则与唯一性推导 | 12 |
| 完成 record 实验 | 18 |
| 验收 | 4 |
| **合计** | **60** |

## 验收标准

- 构造时拒绝重复 label。
- 投影类型与运行值一致。
- 正例、缺失字段反例、空 record 边界通过。

## 可选延伸

- 比较 tuple-list、排序 tuple、dict 三种内部表示对等价判断的影响。

