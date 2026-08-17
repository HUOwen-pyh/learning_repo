# 第 14 晚：Robin Hood 与 Cuckoo 散列

## 学习目标

- 理解 Robin Hood 散列如何压低探测距离方差。
- 掌握 backward-shift deletion 与早停条件。
- 比较 Robin Hood 的探测链与 Cuckoo 的搬迁图。

## 前置回忆

线性探测的 primary clustering 是什么？“离家距离”如何计算？如果新键比槽中键探测得更远，交换会带来什么？

## 精读正文

Robin Hood 散列在线性探测时比较 probe distance：新键若比占位键离其理想槽更远，就交换，继续携带被“抢”的键向后走。它像劫富济贫，通常降低探测长度方差与尾延迟。查找可早停：若当前探测距离已大于槽中键的距离，目标不可能在更后方，因为插入规则不会让“更富”的键挡在它前面。

删除可做 backward shift：空洞之后的键只要不在自己的理想槽，就向前移一格，直到空槽或距离 0。这样无需墓碑并保持早停不变量。低于阈值负载时操作期望常数，最坏仍可线性。

Cuckoo 散列给每键两个或多个候选槽；查找最坏常数，但插入可能沿交替路径踢出键，遇环需重建/换哈希。其分析关联随机图的连通分量和阈值。工程变体常用 bucketized cuckoo。陷阱：Robin Hood 交换时必须连同值一起；环形距离用模；Cuckoo 不能只限制一次搬迁便声称正确。

## 60 分钟安排

- 0–10 分钟：手插入一组碰撞键并标距离。
- 10–27 分钟：证明早停与 backward shift。
- 27–52 分钟：运行 Robin Hood 随机差分测试。
- 52–60 分钟：画 Cuckoo 二分图并标出环。

## 代码任务

运行脚本；加入每次查询的 probe 统计，与第 13 晚线性探测比较最大值。进阶实现双表 Cuckoo，并在超出踢出上限时用新种子重建。

## 验收标准

- backward-shift 删除后所有键仍可查。
- 能解释早停为何安全。
- 能区分 Robin Hood 的尾延迟优化与 Cuckoo 的最坏查询槽数。

## 延伸/原始资料

- Celis, Larson & Munro, [Robin Hood Hashing](https://doi.org/10.1109/SFCS.1985.48)
- Pagh & Rodler, [Cuckoo Hashing](https://doi.org/10.1016/j.jalgor.2003.12.002)（另有[作者论文页 PDF](https://www.rasmuspagh.net/papers/cuckoo-jour.pdf)）
