# 第 11 晚：Treap 与分裂/合并

## 学习目标

- 同时维护键的 BST 次序与随机优先级的堆序。
- 用 `split`/`merge` 组合插入、删除和区间操作。
- 理解随机优先级带来的期望对数高度。

## 前置回忆

一组互异优先级能否唯一决定 Treap？随机排列生成的 BST 高度期望是什么？`split(root, key)` 应返回怎样的两个集合？

## 精读正文

Treap 的键满足 BST 不变量，独立随机优先级满足最小堆不变量。若优先级互异，最小优先级节点必为根，左右子树递归唯一确定；这等价于按随机顺序插入普通 BST，因此高度期望 (O(\log n))，但最坏仍为 (O(n))。随机保证需要优先级独立且难被输入对手操控。

`split(t, x)` 返回键 `< x` 与键 `>= x` 的两棵 Treap；它只沿一条搜索路径重接指针。`merge(a,b)` 的前置条件是 `max(a)<min(b)`，选择优先级更小的根递归合并。二者期望 (O(\log n))，插入可 `split` 后两次 merge，删除可把目标左右子树 merge。维护 size 后可做 rank/select，乃至把隐式下标当键实现序列编辑器。

陷阱：忽略 merge 的键域前置条件；随机优先级碰撞；分裂边界 `<`/`<=` 不一致；变异结构后漏更新 size。脚本拒绝重复键并注入固定 RNG，测试可复现。

## 60 分钟安排

- 0–8 分钟：写两套不变量。
- 8–25 分钟：手跟踪 split 与 merge。
- 25–50 分钟：运行随机操作差分测试。
- 50–60 分钟：实现 rank 或区间切片草图。

## 代码任务

运行 `practice.py`。完成 `rank(key)`；进阶把 key 改为隐式 size，下放 lazy reverse 标记，做可翻转序列。

## 验收标准

- 检查器同时验证 BST、堆序、size。
- split 后集合不丢不重，merge 后恢复。
- 能说明“期望平衡”对随机源的假设。

## 延伸/原始资料

- Seidel & Aragon, [Randomized Search Trees](https://doi.org/10.1007/BF02189309)
- [Open Data Structures: Random Binary Search Trees](https://opendatastructures.org/ods-python/7_Random_Binary_Search_Tree.html)

