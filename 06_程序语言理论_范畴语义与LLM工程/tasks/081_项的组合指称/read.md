# 第 081 晚：项的组合指称与替换引理

## 具体目标

- 给 STLC 子集写环境式组合指称。
- 验证 beta 方程。
- 在有限样本上验证 substitution lemma。

## 前置编号

- 必须完成：071、080
- 入口问题：compositionality 是按语法构造定义，还是事后测试出的经验？

## 必读表（20 分钟，计入总时长）

| 分钟 | 开放权威一手材料与版本 | 精确章节、页码或锚点 | 阅读问题 |
|---:|---|---|---|
| 5–15 | [Andrew M. Pitts, Denotational Semantics（Cambridge 官方讲义）](https://www.cl.cam.ac.uk/teaching/1112/DenotSem/dens-notes-bw.pdf) | §6.2 “Denotations of terms” pp.70–76 | 变量、lambda 和 application 的 semantic clauses 如何使用环境？ |
| 15–25 | [PLFA，Compositional](https://plfa.inf.ed.ac.uk/Compositional/) | 整章的 compositional semantics 与 substitution lemma 相关标题 | 替换引理如何把语法替换转换成环境更新？ |

Pitts PDF 固定为 Cambridge 2011–12 课程讲义发布版；网页采用当前公开章版。页码按正文印刷页，只读规定范围。

## 导读

lambda 的含义是接收语义值并在更新环境中解释 body；application 则把两个子指称组合。替换引理连接语法代换与环境更新，是后续 soundness 的核心。

## 必做推导或证明

按项结构证明 `⟦e[x:=v]⟧ρ = ⟦e⟧(ρ[x↦⟦v⟧ρ])`；至少完整写 Var 和 App 分支。

证明要明确量化的是所有程序、所有上下文还是本脚本的有限样本；三者不能混写。

## Harness / LLM 工程联系

把工具调用 AST 编译成运行函数时，变量绑定对应 service lookup。替换引理说明内联配置与环境注入何时应得到同一行为。

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

- [ ] beta 示例的指称结果正确。
- [ ] 脚本验证 Var/App/Lam 代表性替换案例。
- [ ] 动手改造：加入 let 并从 lambda/application 推导其语义。

## 可选延伸（不计入 60 分钟）

尝试构造变量捕获导致替换引理失败的错误实现。
