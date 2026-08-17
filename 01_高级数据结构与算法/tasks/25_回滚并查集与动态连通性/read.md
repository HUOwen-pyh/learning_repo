# 第 25 晚：回滚并查集与离线动态连通性

## 学习目标

- 区分增量、减量、完全动态与在线/离线连通性。
- 用回滚 DSU 恢复时间线分治状态。
- 把边的活跃时间区间分配到时间线段树。

## 前置回忆

普通 DSU 为什么不能删除边？路径压缩一次会改多少父指针？若一条边在时间 `[l,r)` 活跃，如何让它只在对应查询时存在？

## 精读正文

动态连通性有多个模型：只加边是 incremental，只有删除是 decremental，增删皆有是 fully dynamic；离线算法可预先看到完整操作序列。今天把每条边的 add/remove 配成活跃区间 `[start,end)`，再把区间放入“时间线段树”的 (O(\log T)) 个节点。DFS 时间树时加入该节点的所有边，到叶子回答当时查询，返回时回滚。

回滚 DSU 的 `snapshot` 是历史栈长度；每次成功 union 记录被改根、旧 size 与组件数，回滚弹到快照。不采用路径压缩，因为一次 find 会修改不定数量父指针，记录虽可行却破坏简洁复杂度；按大小合并单独已保证 find (O(\log n))。每条边被加入 (O(\log T)) 次，总时间 (O((T+I)\log T\log n)) 的直接界，常写成相近多对数界。

关键不变量：进入某时间树节点时，DSU 恰含覆盖该节点整个时间段的边；退出后状态恢复到进入前。陷阱：边端点未规范化、重复 add 语义、remove 不存在边、区间右端是否包含、把路径压缩悄悄加回去。

## 60 分钟安排

- 0–10 分钟：把操作序列转成活跃区间。
- 10–28 分钟：模拟 snapshot/rollback。
- 28–52 分钟：运行离线算法并与每时刻 BFS 差分。
- 52–60 分钟：区分它与真正在线完全动态结构。

## 代码任务

运行 `practice.py`；增加“连通分量数”查询。进阶研究 divide-and-conquer over time 的另一种写法，或阅读 Holm–de Lichtenberg–Thorup 在线结构。

## 验收标准

- add/remove/query 混合序列与 BFS 参考一致。
- 能解释回滚版为何禁用路径压缩。
- 能准确陈述离线假设与边的半开活跃区间。

## 延伸/原始资料

- Holm, de Lichtenberg & Thorup, [Poly-Logarithmic Deterministic Fully-Dynamic Algorithms for Connectivity](https://doi.org/10.1145/502090.502095)
- [CP-Algorithms: Deleting from a data structure in O(T(n) log n)](https://cp-algorithms.com/data_structures/deleting_in_log_n.html)

