# 第 078 晚：PCF 的类型与操作语义

## 具体目标

- 实现带闭包和 fix 的 PCF 子集求值。
- 用 fuel 观察递归终止和发散。
- 区分类型错误、运行错误和未在预算内终止。

## 前置编号

- 必须完成：064–077，尤其 070、076
- 入口问题：PCF 比 STLC 新增的递归构造为什么会破坏强规范化？

## 必读表（20 分钟，计入总时长）

| 分钟 | 开放权威一手材料与版本 | 精确章节、页码或锚点 | 阅读问题 |
|---:|---|---|---|
| 5–15 | [Andrew M. Pitts, Denotational Semantics（Cambridge 官方讲义）](https://www.cl.cam.ac.uk/teaching/1112/DenotSem/dens-notes-bw.pdf) | Ch.5 §§5.1–5.4 pp.53–61：PCF syntax/types、substitution、typing 与 evaluation | fix 的求值规则怎样把自身重新送入函数体？ |
| 15–25 | [PLFA，Big-step semantics](https://plfa.inf.ed.ac.uk/BigStep/) | `BigStep` 章的 call-by-value judgement、values 和 derivations | big-step 语义怎样表示终止；它直接记录发散吗？ |

Pitts PDF 固定为 Cambridge 2011–12 课程讲义发布版；网页采用当前公开章版。页码按正文印刷页，只读规定范围。

## 导读

PCF 在 STLC 上加入自然数、条件和一般递归。操作语义给每个构造执行含义；`fix f` 使函数能引用自己，因此良类型不再推出终止。脚本采用环境闭包，避免把捕获替换错误混入主题。

## 必做推导或证明

为 `fix f. λn. ifzero n then 0 else f(pred n)` 在输入 2 上写前两次递归展开；说明 `fix f.f` 为何无有限求值推导。

证明要明确量化的是所有程序、所有上下文还是本脚本的有限样本；三者不能混写。

## Harness / LLM 工程联系

递归 agent/工具工作流即使每一步类型正确，也可能无限循环；类型安全与终止预算是两类保证。

## 严格 60 分钟

| 分钟 | 动作 |
|---:|---|
| 0–5 | 闭卷回答入口问题 |
| 5–25 | 精读两段材料并回答问题 |
| 25–38 | 完成推导/证明 |
| 38–55 | 运行及改造 `practice.py` |
| 55–60 | 对照验收并记录模型边界 |

合计严格为 60 分钟。

## 验收

- [ ] 递归倒计时函数在足够 fuel 下终止。
- [ ] `fix f.f` 触发预算耗尽而非伪造值。
- [ ] 动手改造：加入加法并实现递归求和。

## 可选延伸（不计入 60 分钟）

阅读 Pitts §5.5 前先写两个可能区分函数的程序上下文。
