# 第 28 晚：量子复杂度：BQP、QMA 与查询优势

## 今晚目标

用状态向量模拟少量量子比特，准确区分已证明包含与未知分离。

## 前置回忆（0–5 分钟）

复数向量；概率；线性代数张量积。 不看资料先写下相关定义；不会也先留下猜测，阅读后再用另一颜色修正。

## 精读（5–25 分钟）

BQP 是量子电路在多项式时间、双边有界错误下判定的语言；QMA 是量子证书加量子验证器的类，可类比 NP，但证书是量子态。已知 BPP⊆BQP⊆PP⊆PSPACE，通常相信但未证明 BQP 包含 NP 完全问题。Deutsch–Jozsa、Simon、Shor 展示特定 oracle/代数结构优势；不能泛化为所有搜索。代码用复数状态向量实现 H、相位 oracle 与测量概率，重现一比特 Deutsch 算法。

**今晚唯一要守住的不变量：** 无测量演化保持向量 L2 范数；概率为振幅模平方且总和为 1。

**常见陷阱：** 复制未知量子态；把振幅当概率；声称量子机多项式解决 SAT。

## 代码实战（25–50 分钟）

运行：

```powershell
python practice.py
```

实现常值/平衡 oracle 判别；加入采样验证理论概率。 先读输出，再定位 `# 动手改造`；只改变一个因素并重新运行。不要删掉原有断言。

## 边界测试与复盘（50–60 分钟）

- 50–57 分钟：补一个最小正例、最小反例和一个边界输入。
- 57–60 分钟：闭卷写“定义 / 不变量 / 本例不能证明什么”各一句。
- 验收：每次门后范数约为1；能列出 BQP 已知包含链与开放边界。

## 延伸与原始资料

[Quantum Computation and Quantum Information 出版页](https://www.cambridge.org/core/books/quantum-computation-and-quantum-information/01E10196D0A682A6AEFFEA52D53BE9AE)；[Watrous complexity notes](https://cs.uwaterloo.ca/~watrous/TQI/)

延伸阅读不计入今晚 60 分钟。先完成代码和验收，再按问题需要阅读原文；链接可能更新，引用时记录访问日期。
