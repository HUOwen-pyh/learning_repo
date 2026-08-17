# 第 8 晚：顺序统计 BST

## 学习目标

- 在 BST 上维护子树大小这一增强字段。
- 实现 `select(k)` 与 `rank(key)`。
- 认识“增强定理”：局部可维护摘要如何扩展接口。

## 前置回忆

BST 的左/右子树次序不变量是什么？中序遍历为何有序？插入一个节点会影响哪些节点的子树大小？

## 精读正文

顺序统计树在每个节点保存 `size = 1 + size(left) + size(right)`。BST 不变量（左键小、右键大）保证中序有序，size 不变量让我们无需遍历就知道左侧有多少元素。`select(k)` 比较 (k) 与左子树大小；`rank(x)` 沿搜索路径累加“被整体跳过的左子树 + 当前节点”。两者成本均为 (O(h))。

这体现数据结构增强的通法：摘要若能由节点及孩子摘要在 (O(1)) 时间重算，那么旋转只需更新常数个节点。区间最大、和、端点等也可类似维护。脚本先用朴素 BST 隔离增强思想；若输入有序，高度 (h=n)，查询退化为线性，接下来 AVL/RB/Treap 会解决。

重复键策略必须明确：脚本把重复次数存为 `count`，size 计入次数。陷阱包括更新路径漏掉祖先、rank 的“< x”与“<= x”混淆、删除有两个孩子时只交换键却忘记 count。复杂度写 (O(h)) 比直接写 (O(\log n)) 更诚实。

## 60 分钟安排

- 0–8 分钟：画树并手算 size。
- 8–25 分钟：推导 rank/select 的分支。
- 25–50 分钟：运行插入和随机差分测试。
- 50–60 分钟：添加重复键边界例。

## 代码任务

运行脚本；实现 `count_between(lo, hi)`，目标用两次 rank 完成。进阶：增加删除并在每次操作后递归检查 size。

## 验收标准

- rank/select 与排序列表一致。
- 能写出 size 更新影响的节点集合。
- 能解释为什么增强没有改变渐近高度依赖。

## 延伸/原始资料

- [CLRS 出版社页面（Dynamic order statistics）](https://mitpress.mit.edu/9780262046305/introduction-to-algorithms/)
- [MIT 6.006 Binary Search Trees](https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-fall-2011/resources/lecture-5-binary-search-trees-bst-sort/)

