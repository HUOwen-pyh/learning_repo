# 第 30 晚：综合项目：MiniCDCL、证书与基准报告

## 学习目标

整合解析、传播、学习、重启、模型/证明检查，产出研究式报告。

## 前置回忆（0–5 分钟）

回顾第1–18与28–29晚不变量。 先闭卷写定义和一个最小例子，再读下文纠正。

## 精读正文（5–25 分钟）

最终项目以一个清晰、可测而非极端优化的 MiniCDCL 收束课程。输入小型DIMACS，先预处理，再用 trail+BCP+DPLL/CDCL风格搜索，输出 SAT 模型或教学级 resolution/RUP 证据；独立 verifier 复核。报告记录原/简化规模、decisions、propagations、conflicts、learned、restarts、时间与随机种子，并和穷举/DPLL基线对拍。工程结论标 EXPERIMENT，算法正确性标 THEOREM/INVARIANT，未知与超时标 UNKNOWN。

**核心不变量：** SAT与UNSAT都由独立证据支持；任何资源上限只产生UNKNOWN；报告可由同一命令复现。

**高频陷阱：** 生成器和验证器共享错误逻辑；只报耗时不报实例；超时误作UNSAT。

## 代码实战（25–50 分钟）

在本任务目录运行 `python practice.py`。运行集成脚本的SAT/UNSAT/随机回归，新增一个DIMACS文本实例并保存报告。 找到文件末尾的“动手改造”，每次只改变一个因素，并保留全部断言与固定随机种子。

## 边界测试与验收（50–60 分钟）

50–57 分钟加入最小正例、最小反例与一个边界输入；57–60 分钟闭卷写“定义 / 不变量 / 本实验不能证明什么”各一句。

验收标准：所有内置与随机对拍通过；模型验证；UNSAT由完整搜索或合法证据支持；指标齐全。

## 原始或权威资料

[MiniSat](https://github.com/niklasso/minisat)；[CaDiCaL API](https://github.com/arminbiere/cadical/blob/master/src/cadical.hpp)；[SAT Competition 2025 proceedings](https://satcompetition.github.io/2025/)

延伸阅读不计入今晚 60 分钟；完成验收后再读。公式中的性能结论若来自实验，必须随实例、版本、预算和种子一起记录。
