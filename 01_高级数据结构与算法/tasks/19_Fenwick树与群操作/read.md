# 第 19 晚：Fenwick 树与群操作

## 学习目标

- 从二进制低位块理解 Fenwick 数组。
- 实现点加、前缀和、区间和与前缀下界。
- 识别哪些代数操作允许“两个前缀相减”。

## 前置回忆

整数 `i & -i` 表示什么？区间和如何由两个前缀和得到？若操作是 `min`，能否从两个前缀最小值恢复区间最小？

## 精读正文

1 下标 Fenwick 数组 `tree[i]` 保存长度 `lowbit(i)`、右端为 `i` 的块和。点 `i` 更新时反复 `i += lowbit(i)`，正好访问所有包含该点的上层块；前缀查询反复 `i -= lowbit(i)`，把 `[1..i]` 分解成不重叠块。两者均访问至多 (O(\log n)) 个单元，空间 (O(n))。

区间和 `sum(l..r)=prefix(r)-prefix(l-1)` 依赖加法有逆元；更一般地需要群结构。对 `min` 没有逆操作，普通 Fenwick 不能支持任意点修改后的通用区间最小。若频率非负，前缀和单调，可用二进制 lifting 在 (O(\log n)) 内找最小下标使前缀和达到目标；若存在负频率则这个语义失效。

不变量可用 `tree[i] == sum(a[i-lowbit(i)+1:i+1])` 检查。陷阱：0 下标接口与 1 下标内部转换、`while i` 在传入 0 时、range 边界、lower_bound 对 target<=0 或超过总和的约定。

## 60 分钟安排

- 0–10 分钟：写出 1..16 的 lowbit 与覆盖区间。
- 10–27 分钟：证明更新/查询访问块正确。
- 27–52 分钟：运行随机差分及 lower_bound。
- 52–60 分钟：写下 min 为何不能相减。

## 代码任务

运行脚本；实现 (O(n)) 建树（让每个 `tree[i]` 向 `i+lowbit(i)` 贡献）。进阶用两个 Fenwick 支持区间加、区间和。

## 验收标准

- 点更新/区间和与列表一致。
- 能从二进制解释两个循环方向。
- 能列出 lower_bound 需要的非负性前提。

## 延伸/原始资料

- Peter Fenwick, [A New Data Structure for Cumulative Frequency Tables](https://doi.org/10.1002/spe.4380240306)
- [CPython `bisect` 文档](https://docs.python.org/3/library/bisect.html)（用于理解下界语义）

