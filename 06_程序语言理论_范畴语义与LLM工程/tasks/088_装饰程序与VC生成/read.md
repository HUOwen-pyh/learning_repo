# 第 088 晚：装饰程序与 Verification Conditions

## 具体目标

- 从装饰 while 产生 init、preservation、exit 三类 VC。
- 在有限状态域检查 VC 并报告反例。
- 用错误注释验证失败定位。

## 前置编号

- 必须完成：087
- 入口问题：装饰程序中哪些断言由程序员提供，哪些可以机械产生？

## 必读（20 分钟，计入本晚）

| 分钟 | 开放权威一手材料与版本 | 精确章节或页内标题 | 阅读问题 |
|---:|---|---|---|
| 5–15 | [Software Foundations PLF 7.0，Hoare Logic, Part II](https://softwarefoundations.cis.upenn.edu/plf-current/Hoare2.html) | “Decorated Programs” 与 “Extracting Verification Conditions” | VC generator 怎样把局部注释转换成纯逻辑蕴含？ |
| 15–25 | [Software Foundations PLF 7.0，Hoare Logic, Part II](https://softwarefoundations.cis.upenn.edu/plf-current/Hoare2.html) | 示例 “A Decorated Program” 至 `verification_conditions` 定义/定理 | VC 全部有效为何足以推出原 triple？ |

Software Foundations 使用 7.0 当前版章节；只读列出的标题范围。

## 导读

装饰程序把 proof outline 内嵌到控制流。VC generation 删除命令推理，留下状态谓词间的逻辑义务，交给自动化或人工证明。

## 必做推导 / 证明

为倒计时循环生成三个 VC，并把每个 VC 写成全称量化的状态公式。

必须区分 partial correctness 与 termination；若使用有限状态穷举，明确它只是该有限模型中的结论。

## Harness / LLM 工程联系

对工具工作流做静态检查时，可将 schema、权限和生命周期注释编译成 VC；失败时应报告具体 stage 和反例状态。

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

- [ ] 正确装饰产生三项且全部通过。
- [ ] mutant body 或错误 post 至少击穿一项 VC。
- [ ] 动手改造：让 checker 返回最小反例状态。

## 可选延伸（不计入 60 分钟）

比较 VC generation 与 symbolic execution 的共同点和差异。

