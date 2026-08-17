# 第 065 晚：静态语义：类型规则先于执行

## 具体目标

- 为 Bool/Nat 表达式实现语法导向类型检查。
- 构造良类型、类型错误和未绑定变量案例。
- 用生成的小表达式实验 progress。

## 前置编号

- 必须完成：064 与 050
- 入口检查：progress 定理中的 closed 和 well-typed 两个条件各排除什么反例？

## 必读表（20 分钟，计入总计）

| 分钟 | 开放权威材料及版本 | 精确章节/页码/页内标题 | 阅读问题 |
|---:|---|---|---|
| 5–15 | [Cambridge, Semantics of Programming Languages 2025–26 官方讲义](https://www.cl.cam.ac.uk/teaching/2526/Semantics/notes.pdf) | §2.2 “Typing” pp.24–28；§2.3 collected language pp.29–32 | 类型规则怎样排除算术和布尔运算混用？ |
| 15–25 | [Software Foundations PLF 7.0，Types](https://softwarefoundations.cis.upenn.edu/plf-current/Types.html) | “Typing” 至 “Progress” 和 “Type Preservation” | preservation 的结论为何谈一步归约后的同一类型？ |

材料均来自大学官方课程或教材官方站点；PDF 页码以讲义印刷页码为准。

## 导读

静态语义不是另一种求值，而是对可接受程序的归纳定义。progress 与 preservation 配合得到 type safety：良类型闭项不会进入非值的 normal form。

## 今晚推导 / 证明

完整推导 `if true then 0 else succ 0 : Nat`；再指出 `if 0 then true else false` 无法应用哪条规则。

推导必须写出配置、规则名与规则前提；只写最终值不合格。

## Harness / LLM 联系

Tool schema validation 是静态过滤的工程类比：在进入执行器前排除形状错误。它不能自动保证工具内部语义正确，但能缩小运行时错误面。

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

- [ ] 类型检查器拒绝分支类型不同和 Nat 条件。
- [ ] 对脚本枚举的闭良类型项检查 progress。
- [ ] 动手改造：加入函数类型或 product。

## 可选延伸（不计入 60 分钟）

手写本语言 preservation 的归纳分类。

