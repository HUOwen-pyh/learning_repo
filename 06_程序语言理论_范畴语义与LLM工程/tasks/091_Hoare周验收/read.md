# 第 091 晚：周验收：验证欧几里得除法循环

## 具体目标

- 验证重复减法除法的初始化、保持和退出。
- 覆盖除数为 1、余数 0、被除数小于除数等边界。
- 注入一个加法方向错误的 mutant，确认 invariant 失败。

## 前置编号

- 必须完成：085–090
- 入口问题：商余数算法最关键的不变量如何同时连接初值和当前状态？

## 必读（20 分钟，计入本晚）

| 分钟 | 开放权威一手材料与版本 | 精确章节或页内标题 | 阅读问题 |
|---:|---|---|---|
| 5–15 | [Software Foundations PLF 7.0，Hoare Logic, Part II](https://softwarefoundations.cis.upenn.edu/plf-current/Hoare2.html) | 示例 “Division” / decorated division program 及其 VC | `n = q*d + r` 如何被循环体保持？ |
| 15–25 | [Software Foundations PLF 7.0，Hoare Logic, Part II](https://softwarefoundations.cis.upenn.edu/plf-current/Hoare2.html) | “Formal Decorated Programs” 与 verification correctness theorem | 程序注释、生成 VC 与最终 triple 之间是哪两层可信边界？ |

Software Foundations 使用 7.0 当前版章节；只读列出的标题范围。

## 导读

程序从 `q=0,r=n` 开始，在 `r≥d` 时执行 `r:=r-d; q:=q+1`。核心等式连接输入常量与可变状态，退出条件再给出 `0≤r<d`。

## 必做推导 / 证明

逐行证明 body 保持 `n=q*d+r ∧ r≥0 ∧ d>0`；从 invariant 与 `¬(r≥d)` 推出最终 post。

必须区分 partial correctness 与 termination；若使用有限状态穷举，明确它只是该有限模型中的结论。

## Harness / LLM 工程联系

这是工具状态变换 verification 的完整缩影：初始化契约、循环不变量、退出 post、mutation test。相同方法可用于 tool retry 计数和资源预算。

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

- [ ] 有限域内所有合法 n,d 都满足 VC 和最终 post。
- [ ] 零除数作为前置条件外反例被拒绝。
- [ ] mutant 在脚本中自动产生最小反例。
- [ ] 动手改造：增加 ranking function 检查。

## 可选延伸（不计入 60 分钟）

把 repeated subtraction 替换为二进制长除法，只设计不变量，不实现。

