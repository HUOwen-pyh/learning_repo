# 第 048 晚：子类型、subsumption 与函数变型

## 学习目标

- 区分 typing 与 subtype 两个判断。
- 实现 reflexivity、Top、传递所诱导的基础关系。
- 正确推导箭头参数逆变、结果协变。

## 前置任务

- 第 036–042 晚 STLC 类型安全。
- 第 045 晚记录类型。

## 必读材料（计入今晚 60 分钟）

| 分钟 | 材料 | 版本 | 精确范围 | 带着问题读 |
|---:|---|---|---|---|
| 10 | [Software Foundations — Sub](https://softwarefoundations.cis.upenn.edu/plf-current/Sub.html) | PLF current，页面快照 2026-01 | “The Subsumption Rule” 与 T_Sub 例子 | subsumption 忘掉了什么信息？ |
| 17 | [Software Foundations — Sub](https://softwarefoundations.cis.upenn.edu/plf-current/Sub.html) | PLF current，页面快照 2026-01 | “The Subtype Relation” 的 Structural Rules、Products、Arrows，至参数逆变解释结束 | 为什么函数输入方向必须反过来？ |

## 精读导引

读 `S<:T` 为“任何 S 值都能安全用在需要 T 的地方”。若 `Student<:Person`，接受所有 Person 的函数当然能用于只会传 Student 的位置；反向不安全，因为只接受 Student 的函数未必能处理任意 Person。

## 必须完成的推导

1. 推导 `(Person→Student)<:(Student→Person)`。
2. 用一个仅 Student 才有的字段反驳函数参数协变。
3. 写出 S_Arrow：`T1<:S1` 且 `S2<:T2` 推出 `S1→S2 <: T1→T2`。

结论类型：【基础规则】箭头类型对定义域逆变、对陪域协变；写反会破坏 type safety。

## 与 DeepSeek Harness / LLM 工业应用的联系

直接联系：替换工具实现时，新实现必须接受调用方可能发送的所有输入，并返回调用方承诺可处理的结果。函数变型给出插件/adapter 兼容性的精确方向。

## 60 分钟安排

| 环节 | 分钟 |
|---|---:|
| 必读材料 | 27 |
| 安全替换反例推导 | 13 |
| 完成 subtype 算法 | 16 |
| 验收 | 4 |
| **合计** | **60** |

## 验收标准

- 能口述 `<:` 的可替换含义。
- 参数逆变/结果协变测试通过。
- 正例、错误协变反例、自反边界例齐全。

## 可选延伸

- 给 subtype 返回 proof object，记录使用了 Top/Arrow/Base 哪条规则。

