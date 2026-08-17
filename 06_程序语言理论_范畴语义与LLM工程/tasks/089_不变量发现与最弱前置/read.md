# 第 089 晚：不变量发现与最弱前置条件

## 具体目标

- 为赋值、顺序、条件计算 WP。
- 在有限模型验证 WP 的充分性和最弱性。
- 从候选谓词筛选循环不变量。

## 前置编号

- 必须完成：087–088
- 入口问题：“最弱”是按集合包含还是语句长度衡量？

## 必读（20 分钟，计入本晚）

| 分钟 | 开放权威一手材料与版本 | 精确章节或页内标题 | 阅读问题 |
|---:|---|---|---|
| 5–15 | [Software Foundations PLF 7.0，Hoare Logic, Part II](https://softwarefoundations.cis.upenn.edu/plf-current/Hoare2.html) | “Finding Loop Invariants” | 从 postcondition 倒推、删除不被保持的 conjunct 是怎样的过程？ |
| 15–25 | [Software Foundations PLF 7.0，Hoare Logic, Part II](https://softwarefoundations.cis.upenn.edu/plf-current/Hoare2.html) | “Weakest Preconditions” 与 `is_wp` 定义 | WP 的 sufficiency 和 weakness 两个条件分别是什么？ |

Software Foundations 使用 7.0 当前版章节；只读列出的标题范围。

## 导读

WP 是能保证给定后置条件的最大状态集合，因此逻辑上最弱。对无循环程序可按语法倒推；循环需要不动点或外部 invariant，不能用同一有限公式机械解决所有情况。

## 必做推导 / 证明

计算 `wp(x:=x+1; y:=2*x, y>10)`，逐次做 substitution，化简成初始状态公式。

必须区分 partial correctness 与 termination；若使用有限状态穷举，明确它只是该有限模型中的结论。

## Harness / LLM 工程联系

调用工具前自动倒推 schema/权限要求，能生成最宽松可接受输入；过强条件会不必要地拒绝模型候选。

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

- [ ] 脚本的 WP 与语义 preimage 完全相同。
- [ ] 错误的更宽候选有明确反例。
- [ ] 动手改造：加入 if 并推导分支 WP。

## 可选延伸（不计入 60 分钟）

研究 while 的 weakest liberal precondition 与 total WP 区别。

