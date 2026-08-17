# 第 061 晚：线性逻辑与会话类型：协议即命题

## 具体目标

- 把 send/receive/end 协议表示为递归语法。
- 计算协议对偶。
- 实现每次通信恰好消费一个线性动作的 endpoint。

## 前置编号

- 必须完成：057、060
- 闭卷入口问题：线性假设与普通假设相比，为什么不能任意复制或丢弃？

## 必读（20 分钟，已计入 60 分钟）

| 分钟 | 开放权威一手材料与版本 | 精确章节、页码或页内标题 | 阅读问题 |
|---:|---|---|---|
| 5–15 | [Wadler, Propositions as Sessions，作者版](https://homepages.inf.ed.ac.uk/wadler/papers/propositions-as-sessions/) | 论文 §§1–2：Introduction、Propositions as Types、session propositions 对照表 | 发送、接收和终止分别对应哪些逻辑联结词？ |
| 15–25 | [Wadler 论文开放 PDF](https://www.pure.ed.ac.uk/ws/files/15346790/S095679681400001Xa.pdf) | §3 “Classical Processes”，语法、typing rules 与 cut | channel 名在 typing judgement 中为什么必须线性出现？ |

只读指定边界；链接均为大学官方讲义、作者版本或正式论文页面。

## 导读

会话类型给 channel 规定按顺序发生的动作；对偶把 send 与 receive 交换，使两端能配合。线性使用阻止工具结果被重复消费或必需响应被悄悄丢弃。

## 必做推导 / 证明

给协议 `!Request.?Result.end` 求对偶，并写出两端通过 cut 连接后的归约首步。

必须保留判断形式和规则名；“凭直觉显然”不算完成。

## DeepSeek Harness / LLM 工程联系

一次 tool call 的 request/result/cancel 是有顺序、有唯一关联 id 的协议。会话类型能表达“不能在 result 前再提交同一调用的第二个 result”等时序约束。

这是从形式概念到工程约束的映射；除明确指出外，不宣称 Harness 已静态证明这些性质。

## 严格 60 分钟

| 时间 | 工作 |
|---:|---|
| 0–5 | 回忆入口问题，写定义和反例 |
| 5–25 | 完成必读表并回答两个问题 |
| 25–38 | 手写推导或证明 |
| 38–55 | 运行 `practice.py`，再完成文件顶部的动手改造 |
| 55–60 | 按验收项自测并记录一个疑问 |

5 + 20 + 13 + 17 + 5 = 60 分钟。下面的延伸不得挤入本晚。

## 验收

- [ ] 两次 dual 恢复原协议。
- [ ] 脚本拒绝方向错误、类型错误和 End 后通信。
- [ ] 动手改造：加入 internal/external choice。

## 可选延伸（不计时）

阅读论文 §4 的 propositions-as-sessions translation。

