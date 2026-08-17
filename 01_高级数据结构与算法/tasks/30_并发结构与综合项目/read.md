# 第 30 晚：并发正确性与综合流式索引

## 学习目标

- 用 linearizability 描述并发对象的可观察正确性。
- 区分互斥、lock-free、wait-free 与内存回收问题。
- 综合 Bloom、Count-Min、Trie、堆与不可变快照完成可验证项目。

## 前置回忆

线程安全是否只等于“不会崩溃”？一个复合更新被查询看到一半会怎样？CPython 有 GIL 时为何仍要定义对象级原子性？

## 精读正文

Linearizability 要求每个并发操作看起来在调用与返回之间某一瞬间原子发生，并保持现实时间先后。它是对象的局部性质；不等于数据库事务的多对象原子性。脚本以一个 `Lock` 包住复合更新，获得清晰线性化点：计数、Bloom 位、Count-Min 表、Trie 和 heap 都在同一临界区更新，快照不会观察到半完成状态。GIL 是解释器实现机制，不能替代 API 的同步契约，也不能让多步骤不变量自动原子。

非阻塞进度分层：lock-free 保证系统整体持续完成操作，wait-free 保证每个线程有限步完成；“用了 CAS”不自动满足。删除并发节点还涉及 hazard pointers、epoch reclamation 或 RCU：逻辑删除后，读者仍可能持引用，过早复用内存会产生 ABA/悬空访问。Python GC 遮蔽了部分回收危险，却没有消除竞争语义。

综合项目 `ConcurrentStreamIndex` 的精确字典是事实源；Bloom 提供快速“肯定没见过/可能见过”，Count-Min 展示定长近似频率，Trie 维护不同键的前缀计数，lazy heap 输出 top-k，快照复制成不可变值。不变量包括 CMS 不低估非负频率、Bloom 对已插入键无假阴性、Trie 只给首次出现键加 distinct、heap 条目需与当前精确频率核验以丢弃过期项。

复杂度：一次 add 为 (O(d+L+\log U))，其中 (d) 是 CMS 行数、(L) 是键长、(U) 是不同键数；锁使当前吞吐串行。下一步可按稳定哈希分片，每片独立锁/摘要，但跨片 top-k 与一致快照需要定义较弱语义或协调屏障。前沿方向还包括 learned index、持久内存结构、NUMA-aware、并发 succinct 索引；评估必须同时报告正确性模型、P50/P99、吞吐和内存。

## 60 分钟安排

- 0–10 分钟：给 add/snapshot 标线性化点。
- 10–25 分钟：读综合结构不变量与各组件误差语义。
- 25–50 分钟：运行确定性、并发、差分测试。
- 50–60 分钟：选择一个改造，写一页设计复盘。

## 代码任务

运行 `practice.py`。优先改造为 4 个 shard：明确 `add`、单键查询、全局 top-k、snapshot 各自的一致性。另一方向是保存第 22 晚式不可变快照，让读者无锁读取旧版本。

## 验收标准

- 多线程结束后总数、精确频率、前缀 distinct、top-k 全与参考值一致。
- 已见键无 Bloom 假阴性，CMS 不低估。
- 能画出当前单锁版本的线性化点，并说明分片后哪些操作不再天然原子。
- 复盘包含：工作负载、理论界、实测指标、一个失败用例、一个下一步研究问题。

## 延伸/原始资料

- Herlihy & Wing, [Linearizability: A Correctness Condition for Concurrent Objects](https://doi.org/10.1145/78969.78972)
- Michael, [Hazard Pointers: Safe Memory Reclamation for Lock-Free Objects](https://doi.org/10.1109/TPDS.2004.8)
- [Linux kernel RCU documentation](https://docs.kernel.org/RCU/)
- Kraska et al., [The Case for Learned Index Structures](https://doi.org/10.1145/3183713.3196909)

