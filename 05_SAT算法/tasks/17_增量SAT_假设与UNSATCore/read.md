# 第 17 晚：增量 SAT、假设与 UNSAT Core

## 学习目标

模拟 IPASIR 状态，复用子句库并提取假设下的失败核心。

## 前置回忆（0–5 分钟）

CDCL 根层；模型；最小/非最小核心。 先闭卷写定义和一个最小例子，再读下文纠正。

## 精读正文（5–25 分钟）

增量接口允许永久加入子句，并为一次 solve 临时加入 assumptions。调用结束后假设被重置，永久学习若在正确接口下可复用。若 F∧A 不可满足，可返回 A 的一个子集 core 仍使 F 不可满足；它不一定最小，更不一定最小基数。教学版可用 deletion-based shrinking：逐个尝试移除假设并重求解，得到 subset-minimal core。工业接口如 IPASIR 明确规定 add/assume/solve/val/failed 的状态语义。

**核心不变量：** 假设只对下一次求解有效；返回 core⊆assumptions 且 F∧core UNSAT。

**高频陷阱：** 把永久子句当临时；把 subset-minimal 叫 minimum；SAT 后查询 failed。

## 代码实战（25–50 分钟）

在本任务目录运行 `python practice.py`。实现会话对象和删除式 core，验证移除 core 任一元素后变 SAT。 找到文件末尾的“动手改造”，每次只改变一个因素，并保留全部断言与固定随机种子。

## 边界测试与验收（50–60 分钟）

50–57 分钟加入最小正例、最小反例与一个边界输入；57–60 分钟闭卷写“定义 / 不变量 / 本实验不能证明什么”各一句。

验收标准：连续三次不同假设无串扰；core 可靠且子集最小。

## 原始或权威资料

[IPASIR 接口](https://github.com/biotomas/ipasir)；[CaDiCaL API](https://github.com/arminbiere/cadical/blob/master/src/cadical.hpp)

延伸阅读不计入今晚 60 分钟；完成验收后再读。公式中的性能结论若来自实验，必须随实例、版本、预算和种子一起记录。
