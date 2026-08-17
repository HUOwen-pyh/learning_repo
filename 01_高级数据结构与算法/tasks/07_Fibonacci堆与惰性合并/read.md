# 第 7 晚：Fibonacci 堆与惰性合并

## 学习目标

- 理解“先欠账、后批量整理”的惰性数据结构设计。
- 用势能 (t+2m) 解释插入、meld、decrease-key 的均摊界。
- 理解标记与级联切断如何控制树形。

## 前置回忆

二项堆插入为何会连续进位？如果先把新节点留在根表会怎样？节点连续失去孩子为何危险？

## 精读正文

Fibonacci 堆把二项堆的整理延迟到 `extract_min`。根表可暂有多个同度树；插入和 meld 只拼接根表并更新最小指针，实际 (O(1))。删除最小时才按度链接根，成本与根数和最大度有关。

`decrease_key` 若破坏父子堆序，就把节点切到根表。一个非根节点第一次失去孩子时标记；第二次再失去孩子便把它也切走，向上级联。核心结构不变量是根无父且不标记、父键不大于子键、同一孩子环完整。标记规则保证度为 (k) 的节点子树大小至少按 Fibonacci 数增长，所以最大度 (O(\log n))。

势能取 \(\Phi=t+2m\)：`t` 为根数，`m` 为标记节点数。级联切断的实际工作由减少的标记势能支付，因此 decrease-key 均摊 (O(1))；extract-min 均摊 (O(\log n))。陷阱：这些是均摊而非最坏延迟；真实硬件上复杂指针和大常数常输给二叉堆。Dijkstra 只有大量 decrease-key 且图足够大时才可能受益。

## 60 分钟安排

- 0–10 分钟：对照二项堆列出“立即整理/延迟整理”。
- 10–28 分钟：手算一次切断前后 (t+2m)。
- 28–52 分钟：运行精简但完整的 Fibonacci 堆实验。
- 52–60 分钟：记录理论优势与工程代价。

## 代码任务

脚本持有节点句柄并测试 decrease-key、meld、extract-min。动手统计实际切断次数与势能变化，验证一次长级联的摊还成本。

## 验收标准

- 所有顺序和结构断言通过。
- 能解释没有标记/级联时最大度证明为何失效。
- 能区分操作的实际界、均摊界和工程速度。

## 延伸/原始资料

- Fredman & Tarjan, [Fibonacci Heaps and Their Uses in Improved Network Optimization Algorithms](https://doi.org/10.1145/28869.28874)
- [MIT 6.854 Fibonacci Heaps notes](https://courses.csail.mit.edu/6.854/16/Notes/n1-fibonacci.html)

