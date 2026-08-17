# 第 24 晚：局部搜索、2-opt 与模拟退火

## 学习目标

- 明确定义解编码、邻域、增量评价与局部最优。
- 实现 TSP 2-opt descent 和有种子的模拟退火。
- 设计公平、可复现的启发式实验，不伪装最优性证明。
- 理解 tabu、LNS、iterated local search 的共同框架。

## 前置回忆

可行 TSP tour 是一个排列加回起点。2-opt 删除两条不相邻边并反转中间片段；对称 TSP 中可用四条边的差值 $O(1)$ 评估。

## 完整精读讲解

局部搜索从可行解出发，反复用邻域中更好解替换，直到没有改善。first improvement 每发现改善就走，单轮便宜；best improvement 扫完整邻域，步数可能少。2-opt 局部最优只说明没有单次 2-opt 改善，不代表全局最优，最坏质量仍可差。

模拟退火以概率 $\exp(-\Delta/T)$ 接受变差移动（最小化时 $\Delta>0$），高温探索、降温后趋于贪心。理论上的极慢对数降温可渐近收敛，工程常用几何降温但无最优保证。必须保留 best-so-far，因为当前解可能退化。

更大邻域可跳出局部盆地：3-opt、variable neighborhood、large neighborhood search 先 destroy 再 repair；tabu 禁止近期逆移动；iterated local search 对局部最优做扰动再下降。算法表现依赖编码与增量计算，常比“换一个高级元启发式名字”更重要。

实验至少固定实例集、随机种子、时间/迭代预算，报告多次运行分布、最好/中位/最差、相对已知下界或最优值的 gap。陷阱：只展示最好一次、不同算法预算不等、温度尺度与距离量纲不匹配、2-opt 反转端点错误、累计浮点增量漂移而不定期重算。

## 精确 60 分钟

- 00–07：画一条 2-opt 移动。
- 07–18：推导四边增量公式。
- 18–29：比较 first/best improvement。
- 29–39：理解退火接受率与温度尺度。
- 39–53：运行最近邻、2-opt、退火。
- 53–58：换三个种子记录分布。
- 58–60：写明结果不具何种证明。

## 代码任务

生成固定随机欧氏实例；最近邻构造；2-opt descent；模拟退火。每阶段检查排列可行并完整重算长度，确保 best 不劣于起点。

## 验收标准

- 所有 tour 都恰访问每点一次。
- 2-opt 输出不长于最近邻，退火 best 不长于其起点。
- 相同种子完全复现。
- 报告算法预算和下界/真值缺失，不称“最优”。

## 原始/权威资料

- Croes 1958 2-opt：https://doi.org/10.1287/opre.6.6.791
- Kirkpatrick, Gelatt & Vecchi 1983 simulated annealing：https://doi.org/10.1126/science.220.4598.671
- Pisinger & Ropke 2010 Large Neighborhood Search：https://doi.org/10.1007/978-1-4419-1665-5_13

