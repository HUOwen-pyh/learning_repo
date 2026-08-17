# 第176晚：Cordis 论文——问题与组合性

## 目标与前置

- 目标：精确区分 temporal、spatial 与 algebraic composability，并理解传统 coarse-grained workaround 的边界。
- 前置：动态插件、作用域、依赖图。

## 计入 60 分钟的必读

| 分钟 | 材料 | 版本 | 精确范围 | 问题 |
|---:|---|---|---|---|
| 24 | [A Programming Paradigm for Spatiotemporal Composability](https://github.com/cordiverse/paper/blob/948a07b369c62adb3b12e102458be5c18dfb69b9/paper.pdf) | Cordis paper 948a07b369c62adb3b12e102458be5c18dfb69b9，Draft 2026-08-13 | path paper.pdf；Abstract、§1.1–§1.3，PDF pp.1、4–6；checked_at 2026-08-15 | “移除后恢复”与“依赖变化后响应”分别是什么性质？ |
| 6 | 同一固定 PDF | 同版 | §2 Effects、Coeffects、Relationship，PDF pp.7–8 | 论文怎样把经典静态概念提升为运行时机制？ |

## 阅读导引

每段写一句边栏摘要：问题、反例、现有 workaround、贡献。对 VSCode 与 agent harness 两个动机案例分别列时间维和空间维缺口，不把进程重启误当细粒度组合。

## 核心推导

组件 C 对共享上下文 Γ 产生变换。时间可组合要求移除 C 后能恢复适当的先前观察；空间可组合要求 C 声明的需求随提供者集合变化而响应。两轴正交：可清理但依赖写死，或依赖可发现但无法卸载，都只满足一轴。

## 工业联系与事实标签

- [THEOREM] 由定义可构造四象限：两个布尔性质彼此不蕴含；给出各自单独成立的反例即可证明独立。
- [EMPIRICAL] 论文第1节报告其在 2026-06-09 对 VSCode Marketplace top-100 的观测；这是时间点限定的数据。
- [INFERENCE] 自演化 LLM harness 比普通插件系统更需要可回滚，因为错误组件可能损伤恢复路径本身。
- [OPEN] “完全恢复”应按位相等还是观察等价，需到 §3.3 才精化。

## 严格 60 分钟

- 0–5：画四象限；5–35：逐段精读；35–52：运行有限上下文练习；52–57：各造一个单轴反例；57–60：记录定义。

## 验收

能无混淆定义两轴；代码覆盖可逆、不可逆、空变换；阅读笔记逐段对应指定页。

## 可选延伸

读 §7 Related Work，PDF pp.74–79，不计入本晚。
