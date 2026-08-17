# 第 079 晚：程序上下文与上下文等价

## 具体目标

- 把单孔上下文表示为可组合 frame。
- 在有限上下文族上寻找区分 witness。
- 明确 bounded contextual testing 不是完整判定过程。

## 前置编号

- 必须完成：078
- 入口问题：只比较两个闭项自身的结果，为何不足以定义可替换性？

## 必读表（20 分钟，计入总时长）

| 分钟 | 开放权威一手材料与版本 | 精确章节、页码或锚点 | 阅读问题 |
|---:|---|---|---|
| 5–15 | [Andrew M. Pitts, Denotational Semantics（Cambridge 官方讲义）](https://www.cl.cam.ac.uk/teaching/1112/DenotSem/dens-notes-bw.pdf) | §5.5 “Contextual equivalence” pp.62–63 | closing context 和 observable result 在定义中分别承担什么作用？ |
| 15–25 | [PLFA，Contextual Equivalence](https://plfa.inf.ed.ac.uk/ContextualEquivalence/) | 章首定义至 contextual equivalence 的 congruence/observational clauses | 为什么上下文等价天然包含无限多个上下文的量化？ |

Pitts PDF 固定为 Cambridge 2011–12 课程讲义发布版；网页采用当前公开章版。页码按正文印刷页，只读规定范围。

## 导读

上下文等价把“程序可替换”定义为任何合法程序上下文都观察不到差异。实践只能枚举有界上下文，因此输出 `equivalent` 必须读作“在此测试族中未区分”。

## 必做推导或证明

证明上下文等价是等价关系；传递性中显式保留对任意 closing context 的量化。

证明要明确量化的是所有程序、所有上下文还是本脚本的有限样本；三者不能混写。

## Harness / LLM 工程联系

插件替换兼容性不能只看直接返回，还要观察放入 agent loop、日志、取消和重试上下文后的行为。上下文 witness 是高价值回归测试。

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

- [ ] 脚本找到 0 与 1 的区分上下文。
- [ ] 脚本在指定有界族中无法区分 `0+e` 与 e。
- [ ] 动手改造：生成深度 2 的上下文闭包。

## 可选延伸（不计入 60 分钟）

研究 CIU theorem 的作用，只写一句它减少了什么量化。
