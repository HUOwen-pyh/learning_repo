# 第 29 晚：B-tree、外存模型与 Cache-Oblivious 思想

## 学习目标

- 在 I/O 模型中按块传输次数而非指令计费。
- 理解 B-tree 的占用率、分裂与 (O(\log_B N)) 高度。
- 区分 cache-aware 与 cache-oblivious 设计。

## 前置回忆

若一次磁盘/缓存传输带回 (B) 个键，二叉树一个节点一块会浪费什么？多路节点如何降低高度？满孩子为何要在下降前分裂？

## 精读正文

外存（I/O）模型有内部存储容量 (M) 和块大小 (B)，一次传输整个块，目标最小化 I/O。最小度数 (t) 的 B-tree 每个非根节点有 (t-1\) 到 (2t-1) 个键，内部节点孩子数为键数加一，所有叶深相同。高扇出使高度 (O(\log_t n)\)；若节点尺寸匹配块，即 (O(\log_B n)) I/O。

搜索在节点内定位分支。插入采用 top-down split：下降前若孩子已满，把中间键提升父节点，左右各留 (t-1) 个键，再选择一侧。这样永不递归进入满节点。关键不变量是键有序、孩子分隔键域、占用率合法、叶深一致。删除需要借键/合并来保证下降孩子有足够键，明显更复杂。

B-tree 是 cache-aware：节点大小显式适配 (B)。Cache-oblivious 算法不知道 (M,B)，却用递归布局同时适配多级缓存；van Emde Boas 布局可让静态搜索达到良好块复杂度，funnel sort 在 tall-cache 假设下排序最优。它不等于“忽略缓存”，而是分析对任意块层次成立。陷阱：用 Python 对象节点无法模拟真实块占用；只计比较不计节点/块访问；分裂忘记搬孩子；根是占用率例外。

## 60 分钟安排

- 0–10 分钟：画 `t=2` 的节点上下界。
- 10–28 分钟：手做连续插入和根分裂。
- 28–52 分钟：运行 B-tree 插入/搜索与不变量检查。
- 52–60 分钟：比较节点访问与二叉搜索高度。

## 代码任务

运行 `practice.py`；改变最小度数并记录平均节点访问数。进阶实现 B+ tree 叶链范围扫描，或将静态 BST 按 vEB 顺序布局后模拟块访问。

## 验收标准

- 有序与随机插入后占用率、键域、叶深均正确。
- 搜索与 `set` 差分一致。
- 能解释 (O(\log_B n)) 中的 (B) 来自节点/块扇出。

## 延伸/原始资料

- Bayer & McCreight, [Organization and Maintenance of Large Ordered Indices](https://doi.org/10.1007/BF00288683)
- Aggarwal & Vitter, [The Input/Output Complexity of Sorting and Related Problems](https://doi.org/10.1145/48529.48535)
- Frigo et al., [Cache-Oblivious Algorithms](https://doi.org/10.1145/347837.347852)

