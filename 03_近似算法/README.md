# 近似算法：30 晚 × 60 分钟训练营

这不是“算法目录”，而是一条从 **NP 优化问题的性能保证** 走到 **LP/SDP、随机化、流式与学习增强前沿** 的证明—实现双线课程。每天只需一小时；`read.md` 是当晚必须精读的讲义，`practice.py` 是可直接运行、带断言和小规模精确对拍的实验。

## 使用方式

环境只需 Python 3.11+，不安装第三方包。在本目录运行某一晚：

```powershell
python tasks/01_建模与近似比/practice.py
```

建议固定节奏：先按讲义计时阅读与手推，再运行代码、读断言，最后完成文件末尾的“动手改造”。不要用一次跑通代替证明；近似算法的核心是同时说清 **可行性、时间复杂度、相对 OPT 的界**。

## 30 晚路线图

| 晚 | 主题 | 你要带走的结论/技术 |
|---:|---|---|
| 01 | 建模与近似比 | 最小化/最大化近似比、证书、对拍 |
| 02 | NP 优化与归约下界 | NPO、gap 语言、绝对/渐近保证 |
| 03 | 贪心与交换论证 | 最大覆盖的边际贪心与指数衰减 |
| 04 | 局部搜索与势函数 | 1-flip Max-Cut、终止性、局部最优陷阱 |
| 05 | 集合覆盖 | 加权贪心、调和数 `H_n`、紧例结构 |
| 06 | 顶点覆盖：匹配 | 极大匹配给出 2-近似 |
| 07 | 顶点覆盖：LP | 半整数结构、阈值舍入、整数隙 |
| 08 | metric TSP：双树 | MST 下界与 2-近似、度量闭包 |
| 09 | metric TSP：Christofides | 奇点匹配与 3/2 分析 |
| 10 | 背包 FPTAS | 利润缩放、伪多项式 DP、复杂度—误差权衡 |
| 11 | 经典调度 | list scheduling 与 LPT |
| 12 | 无关机调度 | assignment LP 思想与 2-舍入 |
| 13 | LP 舍入框架 | 整数隙、覆盖/装箱的阈值舍入 |
| 14 | 随机舍入 | 期望、Chernoff/union bound、容量违约 |
| 15 | 条件期望 | pessimistic estimator 与去随机化 |
| 16 | 原始—对偶：覆盖 | 对偶增长、dual fitting |
| 17 | 原始—对偶：网络设计 | Steiner forest/连通需求的 moat growing |
| 18 | `k`-center | Gonzalez 最远优先 2-近似及 2 下界 |
| 19 | 设施选址 | 开设成本 + 连接成本、局部搜索/原始对偶 |
| 20 | Max-Cut 入门 | 随机 1/2 与局部改进 |
| 21 | Max-Cut SDP | Goemans–Williamson 超平面舍入与 0.878… |
| 22 | 流与拥塞 | fractional packing、乘权更新 |
| 23 | 多商品流 | concurrent flow、路径 LP 与 flow-cut gap |
| 24 | 子模贪心 | 基数约束下 `1-1/e` |
| 25 | 连续贪心 | multilinear extension、pipage/swap rounding 入口 |
| 26 | 流式与 sketch | reservoir/AMS、Sieve-Streaming 思想 |
| 27 | 在线近似 | competitive ratio、online set cover/facility 入口 |
| 28 | PCP、UGC 与不可近似性 | gap reduction、阈值、假设边界 |
| 29 | 参数化、细粒度、学习增强 | FPT-AS、Gap-ETH、鲁棒/一致性 |
| 30 | 综合项目 | 自动识别结构并选择算法，生成可核验报告 |

## 阶段验收

- 第 1–10 晚：能独立写出“下界 + 构造 + 收费/交换”的三段式证明，并解释 FPTAS 与 PTAS 区别。
- 第 11–20 晚：能从整数规划写松弛、读对偶，并判断随机化、局部搜索或 primal-dual 哪个更自然。
- 第 21–30 晚：能读研究论文的 theorem/assumption，区分无条件保证、UGC/Gap-ETH 条件下界与经验学习增益。

## 统一实验规范

每个 `practice.py` 都固定随机种子，包含小实例精确算法作为 oracle；规模只用于验证正确性与比值，不能把指数 oracle 当生产算法。浮点比较留容差。你完成“动手改造”后，应保留原断言并增加至少一个会让错误版本失败的新反例。

## 总参考（原始/权威）

- Williamson & Shmoys, *The Design of Approximation Algorithms*, Cambridge, 2011: <https://www.designofapproxalgs.com/book.pdf>
- Vazirani, *Approximation Algorithms*, Springer, 2001: <https://doi.org/10.1007/978-3-662-04565-7>
- Arora & Barak, *Computational Complexity*, Cambridge, 2009（PCP/UGC 背景）: <https://theory.cs.princeton.edu/complexity/book.pdf>
- 课程所有比值默认针对多项式时间算法；前沿结论在对应晚的“资料”中注明假设与论文版本。

