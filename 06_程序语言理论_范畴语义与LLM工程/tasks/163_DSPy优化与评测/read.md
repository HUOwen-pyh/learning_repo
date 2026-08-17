# 第163晚：DSPy 优化与评测

## 目标与前置

- 目标：把 prompt/demo 搜索视为以 metric 为目标的程序优化，并防止验证集泄漏。
- 前置：第162晚、训练/验证划分、离散搜索。

## 计入 60 分钟的必读

| 分钟 | 材料 | 版本 | 精确范围 | 问题 |
|---:|---|---|---|---|
| 11 | [DSPy paper](https://proceedings.iclr.cc/paper_files/paper/2024/file/f1cf02ce09757f57c3b93c0db83181e0-Paper-Conference.pdf) | ICLR 2024 | §3.3 Teleprompters 与 §4 How DSPy Compiles Programs（PDF pp.5–6） | 优化器怎样生成候选并选择程序参数？ |
| 9 | 同上 | 同版 | §5 Goals of Evaluation、§6 GSM8K 与 §7 HotPotQA（PDF pp.6–9），重点读 train/dev/test 划分 | 怎样避免在测试集选 prompt，两个案例的 metric 又有何不同？ |

## 阅读导引

明确 program、candidate、train examples、validation metric、held-out test 五个对象。将每次候选选择记录成可回放实验，而非只保存赢家。

## 核心推导

有限候选集合 H 上经验风险最小化选择 h*=argmax Σ metric(h(xi),yi)。这只保证验证样本上的最优候选；重复调参会对验证集过拟合，需要独立测试集。

## 工业联系与事实标签

- [THEOREM] 有限非空候选集上的实值分数存在最大元。
- [EMPIRICAL] DSPy optimizer 的收益依模型、数据预算与 metric；论文不是跨域保证。
- [INFERENCE] prompt 优化产物应像模型产物一样版本化、评测和回滚。
- [OPEN] 代理 metric 与真实长期业务价值的偏差无法靠搜索自动消除。

## 严格 60 分钟

- 0–5：定义 metric；5–25：必读；25–48：运行候选优化；48–55：制造 validation/test 反转；55–60：写泄漏防线。

## 验收

唯一赢家、并列、空候选失败均断言；能解释 held-out 的作用。

## 可选延伸

阅读论文附录中的 optimizer 设置，不计时。
