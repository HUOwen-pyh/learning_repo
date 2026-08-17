# 第 21 晚：稀疏表与静态 RMQ

## 学习目标

- 预处理幂长区间以实现 (O(1)) 静态 RMQ。
- 理解幂等操作为何允许重叠覆盖。
- 区分普通 Sparse Table 与 Disjoint Sparse Table。

## 前置回忆

长度 (L) 的区间中最大不超过它的 2 次幂是多少？两个长度 (2^k) 的块怎样覆盖任意区间？若两个块重叠，求和会怎样？

## 精读正文

普通 sparse table 预存 `st[k][i] = op(a[i:i+2^k])`，递推由两个半块合并。静态最小值查询 `[l,r)` 取 (k=\lfloor\log_2(r-l)\rfloor)，合并左端块 `[l,l+2^k)` 与右端块 `[r-2^k,r)`。两块可能重叠，但 `min(x,x)=x`，幂等性让重复元素无害，所以查询 (O(1))，预处理 (O(n\log n))。

对 sum、xor 等非幂等操作，重叠会重复贡献。可用不重叠的 (O(\log n)) 幂块，或构建 Disjoint Sparse Table：对每层的分界点预存向左后缀和向右前缀，任意跨分界区间由两个不重叠摘要合并，查询仍 (O(1))（要求结合律，不要求幂等）。

不变量是每个表项确实代表其声明区间。结构完全静态；一次点更新可能影响 (O(n)) 个跨层表项，若有更新应选 Fenwick/线段树。陷阱：空区间、`log2` 浮点误差（用 `bit_length`）、半开边界，以及盲目把 RMQ 模板换成 sum。

## 60 分钟安排

- 0–10 分钟：用两个幂块覆盖几个区间。
- 10–27 分钟：指出重叠对 min/sum 的不同影响。
- 27–52 分钟：运行 RMQ 与静态和查询实验。
- 52–60 分钟：写结构选择表。

## 代码任务

运行 `practice.py`；普通表实现 min，Disjoint Sparse Table 实现 sum。改造为 gcd（普通表）与字符串拼接（disjoint 表），检查操作次序。

## 验收标准

- 所有非空区间与切片朴素值一致。
- 能定义幂等与结合，说明各自用在哪。
- 能说明为何静态 (O(1)) 查询不等于动态也快。

## 延伸/原始资料

- [CP-Algorithms: Sparse Table](https://cp-algorithms.com/data_structures/sparse-table.html)
- Fischer & Heun, [Theoretical and Practical Improvements on the RMQ-Problem](https://doi.org/10.1007/11780441_5)

