# 计算理论：30 晚、每晚 60 分钟

这条路线从“什么是计算”走到现代复杂性研究。它不是 30 篇名词清单：每晚的 `read.md` 给出定义、证明骨架、不变量与常见误区，`practice.py` 用有限、可验证的实验承载抽象概念。所有代码仅依赖 Python 3.11+ 标准库。

## 使用方法

1. 按编号进入 `tasks/NN_主题/`，先不看实现细节，阅读 `read.md`。
2. 在本目录运行：`python tasks/01_模型_编码与增长率/practice.py`。
3. 完成文件末尾“动手改造”，并把三句话写进自己的学习日志：今天的定义、一个不变量、一个仍不确定的问题。
4. 只有达到验收标准才进入下一晚。脚本中的断言是底线，不等于已经理解证明。

每晚固定节奏：0–5 分钟闭卷回忆；5–25 分钟精读；25–50 分钟运行与改造代码；50–57 分钟做边界/反例测试；57–60 分钟复盘。若卡住，60 分钟到点就记录最小反例，次日继续，不用靠熬夜破坏节奏。

## 先修与符号

需要会 Python 的函数、集合、字典、递归，会离散数学中的集合、图、归纳法、概率和基础线性代数。先统一约定：语言是字符串集合；“问题”默认指判定语言；复杂度按编码后的比特长度计算；未经注明的开放问题绝不当作定理。

## 路线图

| 阶段 | 晚次 | 主线 | 阶段产出 |
|---|---:|---|---|
| 可计算模型 | 01–06 | 编码、自动机、正则/CFL、解析 | 能从定义实现识别器并给不变量 |
| 可计算与不可判定 | 07–10 | 图灵机、对角化、归约、层次 | 会写严格归约方向与证明边界 |
| 经典复杂度 | 11–17 | NP 完全、PH、空间、QBF、NL | 能将证书、量词、配置图互译 |
| 随机/计数/证明 | 18–21 | BPP、#P、IP、PCP | 能区别确定性、概率与交互可靠性 |
| 下界视角 | 22–27 | 电路、通信、描述、参数化、细粒度、证明复杂度 | 会标明无条件与条件性下界 |
| 现代边界 | 28–30 | 量子、元复杂度、综合实验 | 产出可复现且不夸大的研究式报告 |

## 30 晚索引

01. [计算模型、输入编码与增长率](tasks/01_模型_编码与增长率/read.md)
02. [DFA：有限状态与正则语言](tasks/02_DFA与正则语言/read.md)
03. [NFA、正则表达式与子集构造](tasks/03_NFA_正则表达式与子集构造/read.md)
04. [Myhill–Nerode、最小化与非正则性](tasks/04_Myhill_Nerode与抽引引理/read.md)
05. [上下文无关文法与下推自动机](tasks/05_CFG与下推自动机/read.md)
06. [CYK 动态规划与 Chomsky 范式](tasks/06_CYK解析与Chomsky范式/read.md)
07. [图灵机、配置与通用计算](tasks/07_图灵机与通用计算/read.md)
08. [不可判定性、停机问题与对角化](tasks/08_停机问题与对角化/read.md)
09. [映射归约、可识别性与 Rice 定理](tasks/09_映射归约与Rice定理/read.md)
10. [时间复杂度、加速与时间层次](tasks/10_时间复杂度与层次定理/read.md)
11. [P、NP、证书与验证器](tasks/11_P_NP与验证器/read.md)
12. [Cook–Levin：把计算历史编码成 SAT](tasks/12_Cook_Levin与计算表CNF/read.md)
13. [NP 完全性与归约工具箱](tasks/13_NP完全归约工具箱/read.md)
14. [coNP、量词交替与多项式层次](tasks/14_coNP与多项式层次/read.md)
15. [空间复杂度与 Savitch 定理](tasks/15_空间复杂度与Savitch/read.md)
16. [PSPACE 完全性与 QBF](tasks/16_PSPACE与QBF/read.md)
17. [NL、ST-CONNECTIVITY 与补闭包](tasks/17_NL_可达性与补闭包/read.md)
18. [随机复杂度：RP、coRP、ZPP 与 BPP](tasks/18_随机复杂度_RP_BPP/read.md)
19. [#P、计数归约与 Valiant 世界](tasks/19_计数复杂度与SharpP/read.md)
20. [交互式证明、算术化与 Sum-check](tasks/20_交互式证明与Sumcheck/read.md)
21. [PCP、局部检验与 Gap 归约](tasks/21_PCP与Gap思想/read.md)
22. [布尔电路、非一致性与 AC⁰ 下界](tasks/22_电路复杂度与AC0下界/read.md)
23. [通信复杂度、矩形与归约](tasks/23_通信复杂度/read.md)
24. [描述复杂度：逻辑刻画复杂度类](tasks/24_描述复杂度与FO模型检查/read.md)
25. [参数化复杂度：FPT、核化与 W 层次](tasks/25_参数化复杂度_FPT与W层次/read.md)
26. [细粒度复杂度：SETH、3SUM 与 APSP](tasks/26_细粒度复杂度_SETH世界/read.md)
27. [证明复杂度：Resolution、宽度与 SAT](tasks/27_证明复杂度与Resolution/read.md)
28. [量子复杂度：BQP、QMA 与查询优势](tasks/28_量子复杂度_BQP与QMA/read.md)
29. [自然证明、MCSP 与元复杂度前沿](tasks/29_电路下界障碍与元复杂度/read.md)
30. [综合项目：可验证的复杂性实验室](tasks/30_综合项目_复杂性实验室/read.md)

## 验收方式

每 5 晚做一次 10 分钟闭卷复述：写出两个定义、一个定理的证明骨架、一个该定理不能推出的结论。第 10/20/30 晚保存脚本输出作阶段基线。总课程通过标准：

- 能独立判断一段“P/NP 已解决”式论证在哪里偷换了模型、量词或归约方向；
- 能为小实例同时产生结果和可独立验证的证据；
- 能准确标注 `THEOREM`、`ASSUMPTION`、`OPEN`、`EXPERIMENT`；
- 能从原论文或作者讲义继续深入，而非依赖二手结论。

## 前沿边界（资料快照：2026-08）

P vs NP、NP vs coNP、一般强电路下界、MCSP 是否 NP 完全等仍是开放问题。本路线第 29 晚以 Natural Proofs 与元复杂度作为研究入口；[ECCC 的元复杂度专题](https://eccc.weizmann.ac.il/keyword/19915/)持续收录论文。2025 年的工作仍把 MCSP 的 NP 完全性明确称为长期开放问题，因此这里的实验只研究极小真值表，绝不声称提供渐近突破。主教材锚点是 [Arora–Barak 免费草稿](https://theory.cs.princeton.edu/complexity/)；更新跟踪以 [ECCC](https://eccc.weizmann.ac.il/) 和 [Theory of Computing](https://theoryofcomputing.org/) 为准。

## 可选的长期升级

30 晚后把每晚扩为一周：第 1 天重做代码，第 2–3 天补证明，第 4 天读原论文，第 5 天实现更大实验。推荐随后学习伪随机性、编码理论、代数复杂度、量子信息或 proof complexity 中任一支线。
