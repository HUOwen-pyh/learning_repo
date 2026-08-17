# 第165晚：SGLang 前缀缓存与结构化生成

## 目标与前置

- 目标：实现 RadixAttention 的核心抽象——压缩前缀树查找与命名空间隔离，并区分它和结构化解码。
- 前置：Trie、KV cache、第151晚。

## 计入 60 分钟的必读

| 分钟 | 材料 | 版本 | 精确范围 | 问题 |
|---:|---|---|---|---|
| 12 | [SGLang paper](https://proceedings.neurips.cc/paper_files/paper/2024/file/724be4472168f31ba1c9ac630f15dec8-Paper-Conference.pdf) | NeurIPS 2024 | §3 RadixAttention（PDF pp.4–6），重点读 radix tree、LRU eviction 与 cache-aware scheduling | 最长共享前缀怎样复用缓存，压缩边何时分裂？ |
| 8 | 同上 | 同版 | §4 Efficient Constrained Decoding with Compressed Finite State Machine（PDF pp.6–7） | grammar/FSM 状态为何不能与 KV 前缀缓存混为一谈？ |

## 阅读导引

用三条请求画 radix tree，标出共享 token 段与边分裂位置。随后把 grammar mask 看作每次生成可选 token 集，不与 KV cache 混为一谈。本晚代码聚焦最小 radix trie 与 namespace 隔离；LRU 和公平调度只保留为延伸，不纳入验收。

## 核心推导

请求 token 序列在 radix tree 中查找最长前缀，命中长度 h 可复用相应 KV；剩余 n−h token 仍需 prefill。压缩 trie 把单分支 token 串存成一条边，插入部分重叠序列时在最长公共前缀处拆边。

## 工业联系与事实标签

- [THEOREM] Trie 中字符串的根到节点路径唯一，因此最长已有前缀定义唯一。
- [EMPIRICAL] 论文的缓存收益为特定请求分布与系统测量。
- [INFERENCE] 缓存键必须含模型、tokenizer 与 prompt 语义版本。
- [OPEN] 多租户隐私与跨请求 KV 复用的安全边界需部署策略证明；公平调度与 LRU 的组合留待系统课程继续研究。

## 严格 60 分钟

- 0–5：画压缩 trie；5–25：必读；25–48：运行 radix trie；48–55：加入 namespace 反例；55–60：说明 KV cache 与 grammar state 的差别。

## 验收

完整命中、部分命中、插入时拆边、空前缀断言通过；缓存不跨 namespace。

## 可选延伸

为节点加入引用计数与确定性 LRU 淘汰，再讨论饥饿规避；不计时。
