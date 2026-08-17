# 第152晚：XGrammar 持久栈与缓存

## 目标与前置

- 目标：理解持久栈共享、上下文无关状态缓存与并行解码的关系。
- 前置：第151晚、不可变数据结构、哈希缓存。

## 计入 60 分钟的必读

| 分钟 | 材料 | 版本 | 精确范围 | 问题 |
|---:|---|---|---|---|
| 12 | [XGrammar paper](https://proceedings.mlsys.org/paper_files/paper/2025/file/5c20ca4b0b20b0bd2f1d839dc605e70f-Paper-Conference.pdf) | MLSys 2025 | §3.2 Persistent Stack 与 §3.3 Context Expansion（PDF pp.5–7） | 分支为何能共享栈尾，context-dependent token 又怎样检查？ |
| 8 | 同上 | MLSys 2025 | §4.1–§4.3（PDF pp.8–10）：mask latency、端到端 serving、消融 | 哪些结论是测量值而非语义保证？ |

## 阅读导引

先画可变栈复制的成本，再画 cons 节点形成的 DAG。区分 grammar compilation cache、PDA configuration cache 和具体请求的运行状态。

## 核心推导

不可变栈 push(x,s) 创建节点 (x,s)，旧栈仍有效。两个 beam 从共同前缀分叉时共享同一个 s，复制成本由 O(depth) 变为 O(1) 新节点；但垃圾回收和哈希键仍需管理。

## 工业联系与事实标签

- [THEOREM] 纯函数式 cons 栈的 push/pop 为 O(1)，历史版本保持可用。
- [EMPIRICAL] XGrammar 的速度结论由论文列出的基准、GPU 和文法测得。
- [INFERENCE] 将缓存键限定为不可变配置能避免跨请求状态污染。
- [OPEN] 高并发下缓存淘汰与编译延迟的联合最优策略取决于工作负载。

## 严格 60 分钟

- 0–5：画 beam 分叉；5–25：必读；25–48：运行持久栈缓存；48–55：加入命中计数；55–60：解释共享不等于可变别名。

## 验收

证明原版本未改变；覆盖空栈 pop；展示两个分支共享 tail。

## 可选延伸

对照 HAMT 的结构共享，不计时。
