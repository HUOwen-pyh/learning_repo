# 第 066 晚：抽象语法上的结构归纳

## 具体目标

- 从 AST 构造器机械地产生证明分支。
- 证明节点数与递归遍历一致。
- 证明 constant folding 保持表达式求值。

## 前置编号

- 必须完成：064–065
- 入口检查：对 AST 做归纳时，归纳假设来自哪些直接子树？

## 必读表（20 分钟，计入总计）

| 分钟 | 开放权威材料及版本 | 精确章节/页码/页内标题 | 阅读问题 |
|---:|---|---|---|
| 5–15 | [Cambridge, Semantics of Programming Languages 2025–26 官方讲义](https://www.cl.cam.ac.uk/teaching/2526/Semantics/notes.pdf) | §3.1 “Abstract syntax and structural induction” pp.35–40 | 结构归纳原则如何由 AST 的归纳定义自动产生？ |
| 15–25 | [Software Foundations LF 7.0，IndPrinciples](https://softwarefoundations.cis.upenn.edu/lf-current/IndPrinciples.html) | “Induction Principles” 与 “Induction Principles for Other Coq Datatypes” | 构造器参数与归纳假设的数量有什么关系？ |

材料均来自大学官方课程或教材官方站点；PDF 页码以讲义印刷页码为准。

## 导读

结构归纳跟随数据的构造方式，而不是跟随表面文本长度。每个递归字段给一个归纳假设。脚本把性质写成有限样本断言，但 read.md 要求的纸面证明必须覆盖所有构造器。

## 今晚推导 / 证明

对 `Lit | Add e e | Neg e` 证明 `eval(fold(e)) = eval(e)`，逐个构造器写基例和归纳步。

推导必须写出配置、规则名与规则前提；只写最终值不合格。

## Harness / LLM 联系

Harness 事件或工具调用若用 discriminated union 表示，任何 projection、redaction、replay 函数的完整性证明都应按事件构造器结构分类。

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

- [ ] 纸面证明覆盖全部三个构造器。
- [ ] 脚本的正确 fold 在嵌套和空操作边界上保持语义。
- [ ] 动手改造：加入乘法并观察必须新增哪些归纳分支。

## 可选延伸（不计入 60 分钟）

在 TypeScript 中用 `never` 写同一 AST 的 exhaustiveness check。

