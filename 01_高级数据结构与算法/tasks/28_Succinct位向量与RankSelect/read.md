# 第 28 晚：Succinct 位向量与 Rank/Select

## 学习目标

- 区分 compact 与 succinct 空间目标。
- 在位向量上实现 `rank1` 与 `select1`。
- 理解小块查表、超块摘要和信息论下界的关系。

## 前置回忆

长度 (n) 的任意位向量至少需要多少 bit 表示？`rank1(i)` 与 `select1(k)` 是否互为逆？Python 整数的 `bit_count` 做了什么？

## 精读正文

位向量 (B[0..n)) 的 `rank1(i)` 返回半开前缀 `B[:i]` 中 1 的个数；`select1(k)` 返回第 (k) 个（0 下标）1 的位置。原始数据需 (n) bit。若索引额外是 (o(n)) bit 且查询常数时间，就达到典型 succinct 目标；仅把布尔对象压成机器字是 compact，但未必 succinct。

经典 Jacobson 思路设置超块和小块：超块存从头累计 rank，小块存相对超块 rank，块内用查表或 word 操作回答。选取随 (\log n) 缩放的块大小可让辅助空间 (o(n))。脚本以 64-bit word 和每词前缀计数实现工程化 rank：查询一个前缀摘要加一次掩码 bit_count，(O(1)) word-RAM；select 用前缀数组二分再在词内找第 k 个 1，(O(\log(n/64)+64))。

稀疏位向量只含 (m) 个 1 时，信息量约为 \(\log_2 {n\choose m}\)，RRR 等结构可逼近零阶熵并保留 rank/select。succinct tree、FM-index、wavelet tree 都以 rank/select 为底座。陷阱：rank 的开/闭约定、select 的 k 从 0 还是 1、末词填充位、把 Python 对象内存误当理论 bit 数。

## 60 分钟安排

- 0–10 分钟：手算一个位串的 rank/select 表。
- 10–28 分钟：画超块/小块/词内三层。
- 28–52 分钟：运行 packed bitvector 差分测试。
- 52–60 分钟：估算原始位与辅助整数数量。

## 代码任务

运行 `practice.py`；把 select 的词内逐位过程改成清除最低位 `x &= x-1`。进阶实现两级摘要，并以“理论 bit”而非 `sys.getsizeof` 推导冗余。

## 验收标准

- 所有 rank/select 与朴素列表一致。
- 能准确陈述半开 rank 和 0 下标 select 约定。
- 能解释脚本是 rank 的工程化原型，而非完整 succinct 证明。

## 延伸/原始资料

- Jacobson, [Space-efficient static trees and graphs](https://doi.org/10.1109/SFCS.1989.63533)
- Raman, Raman & Rao, [Succinct Indexable Dictionaries with Applications to Encoding k-ary Trees](https://doi.org/10.1145/545381.545411)
- [MIT 6.851 succinct structures lecture notes](https://courses.csail.mit.edu/6.851/spring21/lectures/)

