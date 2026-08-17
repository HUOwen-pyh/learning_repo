# 第151晚：XGrammar 的 PDA 与 token mask

## 目标与前置

- 目标：把 CFG 可接受前缀编译为下推自动机状态，并映射为词表 mask。
- 前置：CFG、栈、tokenization。

## 计入 60 分钟的必读

| 分钟 | 材料 | 版本 | 精确范围 | 问题 |
|---:|---|---|---|---|
| 9 | [XGrammar: Flexible and Efficient Structured Generation Engine](https://proceedings.mlsys.org/paper_files/paper/2025/file/5c20ca4b0b20b0bd2f1d839dc605e70f-Paper-Conference.pdf) | MLSys 2025 | §1–§2 | 结构化生成为何需要 mask？ |
| 11 | 同上 | MLSys 2025 | §3.1–§3.3 | PDA 状态怎样处理 token 内多个字符？ |

## 阅读导引

把字符级转移与 token 级 mask 分开：token 合法仅当逐字符消费后仍有至少一个可接受延展。记录词表预处理与在线状态更新各承担什么工作。

## 核心推导

CFG 的递归嵌套需要无界栈；有限自动机一般不足。对当前 PDA 配置 q，mask[t]=1 当 token t 的字符序列存在合法转移到某个可延展配置。mask 是语法状态到词表布尔向量的函数。

## 工业联系与事实标签

- [THEOREM] 一般 CFG 可由等价 PDA 识别。
- [EMPIRICAL] XGrammar 论文在其硬件、模型和文法基准上报告了低开销结构化生成。
- [INFERENCE] mask 生成与模型 forward 解耦可让同一语法引擎服务多种推理后端。
- [OPEN] 超大动态词表与复杂 Unicode 正则下的最优预处理仍依实现而定。

## 严格 60 分钟

- 0–5：回忆 PDA；5–25：必读；25–48：运行 mask；48–55：加入多字符 token；55–60：画状态到 mask 图。

## 验收

正反边界通过；能解释为什么 token 必须逐字符消费。

## 可选延伸

读论文附录的 grammar normalization，不计时。
