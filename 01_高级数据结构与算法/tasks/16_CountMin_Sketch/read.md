# 第 16 晚：Count-Min Sketch

## 学习目标

- 用多行计数表近似点频率。
- 理解单边误差与 ((\varepsilon,\delta)) 概率保证。
- 识别流式摘要的合并条件与攻击面。

## 前置回忆

Bloom filter 的位冲突造成哪类错误？若计数冲突只会增加，估计值应取多行的最小还是平均？两个相同参数的摘要能否逐格相加？

## 精读正文

Count-Min Sketch 有 (d) 行、每行 (w) 个计数器。更新键 (x) 的每行位置；查询取各行计数最小值。每个槽包含目标真实频率加上碰撞噪声，所以在非负更新模型中永不低估。不同独立行让“所有行噪声都大”的概率快速下降。

取 (w=\lceil e/\varepsilon\rceil)、(d=\lceil\ln(1/\delta)\rceil)，对固定查询键，以至少 (1-\delta) 的概率有 \(\hat f_x\le f_x+\varepsilon\|f\|_1\)。保证不是“所有未来自适应查询同时成立”，也依赖哈希假设。更新和查询为 (O(d))，空间 (O(wd))，与键域大小无关。

相同维度、哈希种子的摘要可逐格相加，适合分布式流；参数或种子不同则不能直接合并。conservative update 只增加当前最小的格子，实践中降低误差，但需谨慎区分其证明。陷阱：负更新会破坏单边保证；计数器溢出；用公开弱哈希面对恶意键；把 CMS 直接当 top-k——它只估计给定键，候选发现需另一个机制。

## 60 分钟安排

- 0–10 分钟：画三行冲突并解释取 min。
- 10–28 分钟：推导 `w,d` 与误差事件。
- 28–52 分钟：运行 Zipf 风格流实验。
- 52–60 分钟：检查重频键与轻频键的误差差异。

## 代码任务

运行 `practice.py`；实现 conservative update 并比较平均过估。再把流拆半，合并两个同种子的 sketch，核对与单次构建一致。

## 验收标准

- 所有估计均不低于真实频率。
- 能陈述误差项是总流量而非目标频率的比例。
- 能列出安全合并必须相同的参数。

## 延伸/原始资料

- Cormode & Muthukrishnan, [An Improved Data Stream Summary: The Count-Min Sketch](https://doi.org/10.1016/j.jalgor.2003.12.001)
- [作者 Count-Min Sketch 页面](https://sites.google.com/site/countminsketch/)

