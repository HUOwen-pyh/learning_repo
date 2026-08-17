# 第 087 晚：条件规则与循环不变量

## 具体目标

- 逐轮检查循环不变量。
- 验证三角数循环。
- 构造看似合理但不保持的错误 invariant。

## 前置编号

- 必须完成：085–086
- 入口问题：while 规则为何只能从 invariant 推出退出时 `I∧¬b`？

## 必读（20 分钟，计入本晚）

| 分钟 | 开放权威一手材料与版本 | 精确章节或页内标题 | 阅读问题 |
|---:|---|---|---|
| 5–15 | [Software Foundations PLF 7.0，Hoare Logic](https://softwarefoundations.cis.upenn.edu/plf-current/Hoare.html) | “Conditionals” 与 “While Loops” | 条件规则为什么把 guard 分别合取到两个分支前置？ |
| 15–25 | [Software Foundations PLF 7.0，Hoare Logic, Part II](https://softwarefoundations.cis.upenn.edu/plf-current/Hoare2.html) | “Decorated Programs” 中 while annotation 的解释 | 循环不变量要在进入、保持、退出三个位置满足什么？ |

Software Foundations 使用 7.0 当前版章节；只读列出的标题范围。

## 导读

不变量不是最终目标，而是每轮边界都成立的归纳命题。证明循环先检查初始化，再证明 body 保持，退出时与 guard 的否定合成后置条件。

## 必做推导 / 证明

程序 `s:=0; i:=0; while i<n: i++; s:=s+i`，证明 invariant `s=i(i+1)/2 ∧ 0≤i≤n`。

必须区分 partial correctness 与 termination；若使用有限状态穷举，明确它只是该有限模型中的结论。

## Harness / LLM 工程联系

Agent 循环中的 invariant 可以约束“每个 pending tool call 恰有一个 id”“日志游标不回退”。它必须在每轮和取消路径上保持。

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

- [ ] 正确 invariant 对 n=0 和多个正例逐步保持。
- [ ] 错误 invariant 在最小反例处失败。
- [ ] 动手改造：加入取消分支并重新定义 invariant。

## 可选延伸（不计入 60 分钟）

尝试用 ranking function `n-i` 补充终止证明。

