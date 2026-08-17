# 第 27 晚：后缀数组与 LCP

## 学习目标

- 用倍增排名构建后缀数组。
- 用 Kasai 算法在线性时间构建 LCP。
- 将模式查询转为有序后缀上的二分范围。

## 前置回忆

若已知每个长度 (2^k) 子串的排名，如何比较长度 (2^{k+1})？相邻后缀 LCP 为什么足以支持重复子串问题？删除首字符后 LCP 至少减少多少？

## 精读正文

后缀数组 `SA` 是所有后缀起点按字典序排列的数组，空间连续，常比后缀树易实现。倍增法第 (k) 轮用二元组 `(rank[i], rank[i+2^k])` 排序，得到长度 (2^{k+1}) 前缀的新等价类；当类数为 (n) 即完成。朴素 Python 排序版本为 (O(n\log^2 n)) 的直接上界；用基数排序可达 (O(n\log n))，还有 SA-IS 等线性算法。

Kasai 构造 `lcp[r] = LCP(SA[r-1],SA[r])`。按文本位置遍历时，若当前后缀与下一排名后缀已有 LCP 长度 (h)，移到下一个文本位置后至少可从 `h-1` 继续，因此总字符扩展线性。最长重复子串长度是 LCP 最大值；任意两个后缀 LCP 可化为其排名区间的 RMQ。

模式匹配在 SA 上做两个边界二分，得到以模式为前缀的后缀连续区间，成本 (O(|P|\log n))（朴素比较）；带 LCP 加速可改进。陷阱：空后缀是否纳入、哨兵必须全局最小且不在字母表、切片比较隐藏 (O(n)) 复制、LCP 数组下标约定。

## 60 分钟安排

- 0–10 分钟：手排 `banana` 后缀。
- 10–28 分钟：跟踪倍增排名与 Kasai 的 h。
- 28–52 分钟：运行随机构建/搜索差分。
- 52–60 分钟：找最长重复子串。

## 代码任务

运行 `practice.py`；用第 21 晚 RMQ 支持任意两后缀 LCP。进阶将每轮 tuple sort 换成两次 counting sort。

## 验收标准

- SA 与直接排序后缀一致。
- LCP 与逐字符朴素值一致。
- 能解释 Kasai 的 h 为何总共只增长 (O(n))。

## 延伸/原始资料

- Manber & Myers, [Suffix Arrays: A New Method for On-Line String Searches](https://doi.org/10.1137/0222058)
- Kasai et al., [Linear-Time Longest-Common-Prefix Computation in Suffix Arrays](https://doi.org/10.1007/3-540-48194-X_17)

