# 第182晚：Cordis 论文——实现对应、边界与验收

## 目标与前置

- 目标：将形式对象映射到 Cordis core/loader，审查 case study 与 discussion 的系统边界。
- 前置：第169–181晚。

## 计入 60 分钟的必读

| 分钟 | 材料 | 版本 | 精确范围 | 问题 |
|---:|---|---|---|---|
| 24 | [Cordis paper](https://github.com/cordiverse/paper/blob/948a07b369c62adb3b12e102458be5c18dfb69b9/paper.pdf) | 948a07b369c62adb3b12e102458be5c18dfb69b9 | path paper.pdf；§5.1 Core Library 与 §5.2 Component Loader，PDF pp.54–66；checked_at 2026-08-15 | effect/coeffect/fiber/config reconciliation 分别落在哪个机制？ |
| 10 | 同一固定 PDF | 同版 | §6.1 System Boundary、§6.3 Access Control and Sandboxing、§6.6 Dependency Typing and Versioning，PDF pp.67、69、72 | 哪些问题明确不由 composability 自动解决？ |
| 4 | 同一固定 PDF | 同版 | §8 Conclusion，PDF p.79 | 论文最终声称的范围是什么？ |

## 阅读导引

做“形式对象→实现机制→未证明假设”三列表。case study 属于实证/说明材料，不能替代语义定理；discussion 是边界和未来方向，不读成已经实现。

## 核心推导

effect tracking 对应 fiber-owned cleanup；coeffect resolution 对应 service visibility/change notification；component lifecycle 对应 fiber states；loader 对应配置树 reconcile/HMR。安全、授权与 OS 隔离是正交机制，时空可组合性不能自动提供。

## 工业联系与事实标签

- [THEOREM] §4 的元理论只在其抽象模型和显式前提内成立，§5 的实现描述不自动构成 refinement theorem。
- [EMPIRICAL] §5.3 Koishi 是 case study；论文无权由单一案例推出所有插件生态的普适性能。
- [INFERENCE] Harness 可利用 composability 降低替换成本，但仍需 tool policy、sandbox、session replay 与 eval。
- [OPEN] §6 明确讨论 system boundary、access control、dependency typing/versioning 等未闭合设计空间。

## 严格 60 分钟

- 0–5：建映射表；5–43：三段精读；43–55：运行属性验收；55–58：列三个非保证；58–60：论文周结论。

## 验收

能映射四个核心机制；断言含 recovery/reactivity/边界；列出安全非保证；所有引用固定到完整 SHA。

## 可选延伸

读 §5.3 和 §7 全文，PDF p.66 已包含在必读尾页，其余 pp.74–79 不计入本晚。
