# 第 085 晚：断言、状态与 Hoare 三元组

## 具体目标

- 把 assertion 表示为状态谓词。
- 用终止执行定义 partial-correctness triple。
- 构造有效、无效和前置条件为空的 triple。

## 前置编号

- 必须完成：064–077，特别是 IMP 解释器 077
- 入口问题：`{P} c {Q}` 对不终止执行作出什么承诺？

## 必读（20 分钟，计入本晚）

| 分钟 | 开放权威一手材料与版本 | 精确章节或页内标题 | 阅读问题 |
|---:|---|---|---|
| 5–15 | [Software Foundations PLF 7.0，Hoare Logic](https://softwarefoundations.cis.upenn.edu/plf-current/Hoare.html) | “Assertions” 至 “Hoare Triples” | assertion、程序状态和 triple validity 的量词分别是什么？ |
| 15–25 | [C. A. R. Hoare, An Axiomatic Basis for Computer Programming](https://doi.org/10.1145/363235.363259) | §2 Axioms and rules of inference，尤其赋值公理的原始陈述 | 为什么赋值规则中的前置条件是对后置条件做替换？ |

Software Foundations 使用 7.0 当前版章节；只读列出的标题范围。

## 导读

Hoare triple 不预测执行过程；它规定从满足 P 的状态出发，若命令终止，则终态满足 Q。对确定、总终止的简单命令可直接穷举有限状态检查，但一般证明依赖规则系统。

## 必做推导 / 证明

对 `x:=x+1` 和后置 `x>0` 计算替换前置条件；证明 `{x≥0} x:=x+1 {x>0}`。

必须区分 partial correctness 与 termination；若使用有限状态穷举，明确它只是该有限模型中的结论。

## Harness / LLM 工程联系

工具执行前置条件可表达 schema 之外的状态要求，后置条件表达对 session/tool state 的保证。timeout 并不自动反驳 partial correctness。

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

- [ ] 能口述 triple validity 的完整量词。
- [ ] 脚本区分有效、无效和 vacuous triple。
- [ ] 动手改造：加入交换两个变量的顺序命令。

## 可选延伸（不计入 60 分钟）

把 total correctness 额外需要的终止条件写成一句形式化陈述。

