# 第 086 晚：Skip、赋值、顺序与后果规则

## 具体目标

- 把 proof rule 证书表示成树。
- 局部检查 Skip、Assignment、Sequence。
- 用 consequence 调整强弱断言。

## 前置编号

- 必须完成：085
- 入口问题：sequencing rule 的中间断言为何是证明接口？

## 必读（20 分钟，计入本晚）

| 分钟 | 开放权威一手材料与版本 | 精确章节或页内标题 | 阅读问题 |
|---:|---|---|---|
| 5–15 | [Software Foundations PLF 7.0，Hoare Logic](https://softwarefoundations.cis.upenn.edu/plf-current/Hoare.html) | “Proof Rules” 下 `Skip`, `Assignment`, `Consequence`, `Sequencing` | consequence rule 中前置与后置蕴含的方向分别怎样？ |
| 15–25 | [Coq 源码对应的 Hoare.v（SF 官方页面内链接）](https://softwarefoundations.cis.upenn.edu/plf-current/Hoare.html) | 定理 `hoare_asgn`, `hoare_skip`, `hoare_seq`, `hoare_consequence` | 规则可靠性的证明分别展开了哪一个语义定义？ |

Software Foundations 使用 7.0 当前版章节；只读列出的标题范围。

## 导读

Hoare 规则把全局语义有效性分解成可组合证书。顺序规则的中间断言像模块接口：前一段保证它，后一段依赖它。consequence 则允许加强前置、减弱后置。

## 必做推导 / 证明

推导 `{x=0} x:=x+1; x:=x+1 {x=2}`，明确写出中间断言。

必须区分 partial correctness 与 termination；若使用有限状态穷举，明确它只是该有限模型中的结论。

## Harness / LLM 工程联系

多阶段 tool pipeline 的每个 stage 可以声明 state contract；中间断言使局部替换不必重新分析整个 pipeline。

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

- [ ] 证书检查器接受合法顺序证明。
- [ ] 错误赋值公理和断裂中间断言被拒绝。
- [ ] 动手改造：显式加入 consequence 证书节点。

## 可选延伸（不计入 60 分钟）

把同一程序用不同强度的中间断言证明两次。

