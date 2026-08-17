# 第 049 晚：记录宽度/深度子类型与综合项目

## 学习目标

- 实现 record width、depth 与 permutation subtyping。
- 用 subsumption 检查“富记录可用于窄接口”。
- 将前七周的 AST、typing、测试不变量汇成小型 schema checker。

## 前置任务

- 第 045 晚“记录类型、标签与投影”。
- 第 048 晚“子类型、subsumption 与函数变型”。

## 必读材料（计入今晚 60 分钟）

| 分钟 | 材料 | 版本 | 精确范围 | 带着问题读 |
|---:|---|---|---|---|
| 20 | [Software Foundations — Sub](https://softwarefoundations.cis.upenn.edu/plf-current/Sub.html) | PLF current，页面快照 2026-01 | “The Subtype Relation” → “Records”：width/depth/permutation 与合并后的 S_Rcd | 为什么字段更多的记录反而在 `<:` 左边？ |
| 7 | [Software Foundations — Sub](https://softwarefoundations.cis.upenn.edu/plf-current/Sub.html) | PLF current，页面快照 2026-01 | 回读 “The Subsumption Rule” 的 record example | 何时可以安全忘掉额外字段？ |

## 精读导引

将 record type 规范成 label→type 映射。判 `S<:T` 时，遍历 T 的每个必需 label：S 必须含它且字段类型为其子类型；S 的其他字段忽略。字段排列不应影响结果。

## 必须完成的推导

1. `{name:String,age:Nat,gpa:Nat}<:{name:String,age:Nat}`。
2. `{owner:Student}<:{owner:Person}`（给定 Student<:Person）。
3. 反驳 `{name:String}<:{name:String,age:Nat}`。

结论类型：【结构子类型规则】记录在字段集合上宽度“反向”、在只读字段类型上深度协变，并忽略排列。

## 与 DeepSeek Harness / LLM 工业应用的联系

直接工程联系：Harness 的工具实现可以返回比公共 schema 更多的诊断字段，只要所有必需字段存在且类型兼容；消费者不应依赖未声明字段。对可写字段，简单深度协变不再安全，需不变或读写能力分离。

## 60 分钟安排

| 环节 | 分钟 |
|---|---:|
| 必读材料 | 27 |
| 三个 subtype 推导 | 11 |
| 完成 schema checker | 18 |
| 验收 | 4 |
| **合计** | **60** |

## 验收标准

- width、depth、permutation 各有测试。
- 缺必需字段必失败；额外字段可安全忘却。
- 输出明确列出 inferred 与 expected schema。

## 可选延伸

- 给字段加入 readonly/writeonly 能力，推导各自 variance。

