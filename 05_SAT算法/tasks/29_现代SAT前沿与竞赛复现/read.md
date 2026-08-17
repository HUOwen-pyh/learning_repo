# 第 29 晚：现代 SAT 前沿：竞赛、外部传播与可验证求解

## 学习目标

读懂当前求解器生态，设计不夸大的 ablation 实验。

## 前置回忆（0–5 分钟）

CDCL全栈；proof logging；统计实验。 先闭卷写定义和一个最小例子，再读下文纠正。

## 精读正文（5–25 分钟）

截至资料快照 2026-08，CaDiCaL 继续以可读、可扩展 CDCL 为重要基线，并提供 IPASIR/外部传播接口；SAT Competition 2025 主赛道要求 UNSAT proof，说明可验证性已是工程标准。前沿包含 inprocessing、vivification、chronological backtracking 混合、局部搜索/CDCL协作、GPU/并行、机器学习分支与证明日志压缩。新方法必须和强基线做 ablation，控制硬件/超时/随机种子，用 PAR-2、solved count 等指标；神经方法的训练成本也要计入。

**核心不变量：** 前沿性能主张绑定版本、数据集、预算和证书；开放/实验结论不包装成定理。

**高频陷阱：** 在小自选数据胜出就称SOTA；比较不同proof要求；忽略训练/预处理成本。

## 代码实战（25–50 分钟）

在本任务目录运行 `python practice.py`。在内置实例族比较三启发式，生成CSV式ablation并用模型/证明复核答案。 找到文件末尾的“动手改造”，每次只改变一个因素，并保留全部断言与固定随机种子。

## 边界测试与验收（50–60 分钟）

50–57 分钟加入最小正例、最小反例与一个边界输入；57–60 分钟闭卷写“定义 / 不变量 / 本实验不能证明什么”各一句。

验收标准：实验可复现；至少一项负结果被如实保留；知道竞赛输出状态10/20/0。

## 原始或权威资料

[SAT Competition 2025](https://satcompetition.github.io/2025/)；[CaDiCaL](https://github.com/arminbiere/cadical)；[2025 输出/证明规则](https://satcompetition.github.io/2025/output.html)

延伸阅读不计入今晚 60 分钟；完成验收后再读。公式中的性能结论若来自实验，必须随实例、版本、预算和种子一起记录。
