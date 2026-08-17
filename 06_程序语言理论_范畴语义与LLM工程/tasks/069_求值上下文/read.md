# 第 069 晚：求值上下文：把顺序写成语法

## 具体目标

- 定义 frame、context、plug 和 decompose。
- 验证 `plug(context, focus)` 重构原项。
- 用上下文实现左到右 CBV 一步归约。

## 前置编号

- 必须完成：064、068
- 入口检查：`E[e]` 中 hole 的唯一性为何重要？

## 必读表（20 分钟，计入总计）

| 分钟 | 开放权威材料及版本 | 精确章节/页码/页内标题 | 阅读问题 |
|---:|---|---|---|
| 5–15 | [Cambridge, Semantics of Programming Languages 2025–26 官方讲义](https://www.cl.cam.ac.uk/teaching/2526/Semantics/notes.pdf) | §5.4 “Evaluation contexts” pp.77–82 | 求值上下文如何用一条 congruence rule 替代多条传播规则？ |
| 15–25 | [Felleisen & Hieb, The Revised Report on the Syntactic Theories of Sequential Control and State](https://doi.org/10.1016/0304-0208(92)90014-7) | §2 evaluation contexts 与 reduction relations 的定义 | decomposition 为何需要唯一 redex 才给出确定策略？ |

材料均来自大学官方课程或教材官方站点；PDF 页码以讲义印刷页码为准。

## 导读

上下文把“下一处归约发生在哪里”从规则集合提升为语法对象。decompose 得到上下文和 redex，contract 只处理核心归约，plug 再放回去。

## 今晚推导 / 证明

对 `(1+2)+(3+4)` 写唯一分解 `E[r]`；证明当前语法的 plug/decompose round-trip，按表达式结构分类。

推导必须写出配置、规则名与规则前提；只写最终值不合格。

## Harness / LLM 联系

流式 agent pipeline 中的中间件栈也是某种运行上下文，但这里只取结构化分解的思想。显式 frame 有助于准确恢复暂停点和取消位置。

## 严格 60 分钟

| 时段 | 任务 | 输出 |
|---:|---|---|
| 0–5 | 闭卷回答入口问题 | 定义和一个反例 |
| 5–25 | 按必读表精读 | 两个问题各 2–3 句 |
| 25–38 | 完成推导/证明 | 可检查的规则树或归纳步骤 |
| 38–55 | 运行并改造 `practice.py` | 正反/边界断言全通过 |
| 55–60 | 按验收清单复盘 | 一条不变量和一个疑问 |

合计 5 + 20 + 13 + 17 + 5 = 60 分钟。

## 验收

- [ ] round-trip 对嵌套项成立。
- [ ] 左右求值次序由 context grammar 唯一决定。
- [ ] 动手改造：加入右到左策略并展示 trace 差异。

## 可选延伸（不计入 60 分钟）

阅读讲义 §5.4 后半的 store/evaluation-context 组合。

