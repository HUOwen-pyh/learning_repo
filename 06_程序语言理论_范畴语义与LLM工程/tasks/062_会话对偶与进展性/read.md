# 第 062 晚：会话对偶、通信归约与进展性

## 具体目标

- 实现双方 action 的同步归约。
- 检查每个非终止配置要么前进、要么给出精确 mismatch。
- 区分协议局部类型正确和全局无死锁。

## 前置编号

- 必须完成：061
- 闭卷入口问题：协议两端分别良类型，为何还需要对偶关系才能推出进展？

## 必读（20 分钟，已计入 60 分钟）

| 分钟 | 开放权威一手材料与版本 | 精确章节、页码或页内标题 | 阅读问题 |
|---:|---|---|---|
| 5–15 | [Wadler, Propositions as Sessions PDF](https://www.pure.ed.ac.uk/ws/files/15346790/S095679681400001Xa.pdf) | §§3–4 中 reduction、type preservation 与 progress/cut elimination 相关命题 | 通信一步如何同时消费两个对偶 action？ |
| 15–25 | [Honda, Vasconcelos & Kubo, Language Primitives and Type Discipline for Structured Communication-Based Programming](https://doi.org/10.1007/BFb0053567) | §2 session structures 与 §3 typing discipline | 最初的 session typing 如何限制 channel 的顺序使用？ |

只读指定边界；链接均为大学官方讲义、作者版本或正式论文页面。

## 导读

最小二方模型中，对偶足以让首动作匹配；一般并发系统还需要处理循环等待，因此不要把本脚本的 progress 外推成任意网络的 deadlock freedom。边界例专门展示双方都结束。

## 必做推导 / 证明

对 send/receive 情形证明一步归约保持剩余协议对偶；写出双方都 send 的 stuck 反例。

必须保留判断形式和规则名；“凭直觉显然”不算完成。

## DeepSeek Harness / LLM 工程联系

并发 tool execution 若只有单端 schema 检查，仍可能在生命周期上互相等待。将 producer/consumer 事件序列成对检查，能发现“各自合法、组合后卡住”的错误。

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

- [ ] 对偶 trace 每步推进直到双方 End。
- [ ] 双方 send 和 payload 类型冲突均被拒绝。
- [ ] 动手改造：加入显式 cancel 分支并保持对偶。

## 可选延伸（不计时）

研究 multiparty session types 的 global/local projection，只记录其额外解决的问题。

