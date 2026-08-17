# 第 090 晚：Hoare 逻辑的模型论、可靠性与相对完备性

## 具体目标

- 区分模型有效与规则可导。
- 在有限 loop-free 模型穷举验证 soundness/completeness。
- 理解一般相对完备性依赖 assertion language 表达力。

## 前置编号

- 必须完成：085–089
- 入口问题：soundness 与 completeness 的量词方向分别是什么？

## 必读（20 分钟，计入本晚）

| 分钟 | 开放权威一手材料与版本 | 精确章节或页内标题 | 阅读问题 |
|---:|---|---|---|
| 5–15 | [Software Foundations PLF 7.0，Hoare Logic as a Logic](https://softwarefoundations.cis.upenn.edu/plf-current/HoareAsLogic.html) | “Hoare Logic and Model Theory” 与 “Hoare Logic and Proof Theory” | semantic validity 与 derivability 使用了哪两个不同关系符号？ |
| 15–25 | [Software Foundations PLF 7.0，Hoare Logic as a Logic](https://softwarefoundations.cis.upenn.edu/plf-current/HoareAsLogic.html) | “Soundness and Completeness” 全节 | 为什么标准 Hoare 逻辑通常只声称相对于 assertion theory 完备？ |

Software Foundations 使用 7.0 当前版章节；只读列出的标题范围。

## 导读

可靠性说每个可导 triple 都语义有效；完备性说每个语义有效 triple 都可由规则导出。有限总函数模型允许把 assertion 当状态集合，直接计算精确 WP，从而实验双向关系。

## 必做推导 / 证明

写出 soundness 和 completeness 两个公式，标出 quantification over P,c,Q；解释 relative completeness 中 oracle/基础理论的位置。

必须区分 partial correctness 与 termination；若使用有限状态穷举，明确它只是该有限模型中的结论。

## Harness / LLM 工程联系

自动评测器的规则证书必须 sound；若不 complete，可能拒绝正确 workflow。工程上需区分 false negative 与真正违规。

## 严格 60 分钟

| 时段 | 内容 |
|---:|---|
| 0–5 | 闭卷回答入口问题并写一个错误 triple |
| 5–25 | 完成必读和两个阅读问题 |
| 25–38 | 手算规则、VC 或 WP |
| 38–55 | 运行并完成 `practice.py` 顶部改造 |
| 55–60 | 对照验收，记录一个 invariant |

严格合计 60 分钟；延伸不计时。

## 验收

- [ ] 脚本对所有有限谓词对验证两方向。
- [ ] 错误 proof rule 产生 soundness 反例。
- [ ] 动手改造：把状态域扩为两个布尔变量。

## 可选延伸（不计入 60 分钟）

阅读 Cook 相对完备性结果的原始定理陈述。

