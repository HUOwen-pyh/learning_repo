# 程序语言理论、范畴语义与 LLM 工程：196 晚路线

这是一条 **28 周 × 7 晚 = 196 晚**、每天 60 分钟的顺序课程。目标不是背诵术语，而是获得三类可检查能力：

1. 能对语言的语法、类型和动态语义写出判断规则，并解释 progress、preservation、组合性和上下文等价；
2. 能从半群、幺半群、函子、自然变换、伴随走到 Monad、代数效应、Handler、Coeffect 与可撤销 effect，知道每一步的定义和定律；
3. 能在固定源码版本上追踪 DeepSeek Harness 的启动、插件装载、一次 turn、LLM stream、工具执行和 session replay，并设计、实现和测试一个 Cordis 插件。

“完全理解项目”在本课程中的可验收含义是：可以闭卷重画关键调用链；为任一核心组件说出类型契约、生命周期和不变量；能修改扩展点而不直接侵入 agent loop；能用相关测试证明卸载、失败、取消和 replay 没有破坏语义。它不是对未来所有 `master` 版本永久有效的承诺。

## 固定研究快照

DeepSeek Harness 明确处于 developer preview，可能发生破坏兼容的变化。因此源码任务固定在以下快照；完成课程后再单独做 upstream delta：

| 对象 | 固定版本 | 核验日期 | 用途 |
|---|---|---|---|
| DeepSeek Harness | [`47f943859bef60e4160492346772ded9b24f765a`](https://github.com/deepseek-ai/deepseek-harness/tree/47f943859bef60e4160492346772ded9b24f765a) | 2026-08-15 | 架构、Cordis 教程、核心包与测试 |
| Cordis 论文 | [`948a07b369c62adb3b12e102458be5c18dfb69b9`](https://github.com/cordiverse/paper/tree/948a07b369c62adb3b12e102458be5c18dfb69b9) | 2026-08-15 | 时空可组合性的形式模型 |

源码阅读必须使用包含完整 commit 的永久链接，并注明文件、符号或行范围。论文必须注明 draft 日期、页码、定义或定理；上游网页文档要记录核验日期。

## 为什么需要数学与程序语言理论

这些概念不是给项目强贴标签，而是用来回答真实工程问题：

| 理论工具 | 能回答的工程问题 |
|---|---|
| 半群、幺半群、同态 | 日志、配置片段和增量结果何时能无歧义组合？ |
| ADT、和类型、穷尽检查 | session event、工具结果和失败状态是否完整建模？ |
| 操作语义、抽象机 | 一次 turn/step/tool call 到底允许怎样迁移？ |
| Hoare 逻辑、精化与会话类型 | 工具前置条件、权限和协议顺序如何表达与检查？ |
| 函子、自然变换、伴随、Monad | 状态、失败、异步与上下文计算怎样保持组合律？ |
| 代数效应与 Handler | 模型、工具、策略、遥测和审批怎样成为可替换处理器？ |
| Coeffect | 插件需要哪些上下文能力，依赖变化时应如何响应？ |
| 可撤销 effect | 插件卸载或 HMR 后为什么不应残留服务、监听器和工具？ |
| CFG/PDA 与类型化 schema | 结构化生成和工具参数如何在生成阶段受约束？ |
| 事件溯源与投影 | session 如何 replay、fork、审计并重建模型可见历史？ |

Cordis 论文确实以 effect、coeffect、统一 context 和动态 component calculus 为中心；Monad 则是学习计算效应语义的重要数学路线。课程会讲清两者联系与差别，不声称 Harness 源码直接声明了一个 `Monad` 类型。

## 每晚严格 60 分钟

- 0–5 分钟：闭卷写出前一天的一个定义、定律或状态不变量。
- 通常 5–25 分钟：阅读 `read.md` 指定的**外部原文精确范围**；证明周、论文周和源码审计夜可延长到第 40–43 分钟。每晚以任务文件里的闭合时间表为准。
- 阅读结束后至第 55 分钟：运行并修改当晚的 `practice.py` 或 `practice.ts`，加入最小正例、最小反例和一个边界用例；原文较重的夜晚会使用更小但可检查的实验。
- 55–60 分钟：完成验收并写三句复盘。

每篇 `read.md` 都必须给出材料版本、章节/页码/源码符号、预计分钟和带着什么问题读。教材首页、整本书、整门课和浮动 `master` 链接不能算作指定精读。

## 双层实战与证据门槛

本课程把“可独立运行的语义模型”和“在目标系统中工作”视为两种不同证据，前者不能代替后者：

| 晚次 | 第一层：独立模型 | 第二层：固定 Harness checkout | 完成条件 |
|---:|---|---|---|
| 162–168 | 运行当晚 `practice.ts`，用最小实现检查 TypeScript 类型、事件、服务和工具契约 | 尚不要求接入 Harness | `node practice.ts` 的断言全部通过；这些文件只是契约预检，不冒充 Harness 实现 |
| 169–175 | 运行当晚 `practice.ts`，先排除概念模型中的错误 | 在同一个 `tmp/cordis-tutorial` 工作区逐章完成官方 Cordis 教程，并运行仓库给出的真实 launcher | 本地断言与真实 checkout 证据必须同时通过；缺一项不得勾选 |
| 183–189 | 运行当晚的最小可执行调用链模型 | 在固定源码中跟踪真实符号，并运行相应定向测试、入口或 trace | 提交永久源码链接、实际命令、退出码与关键输出，不以阅读摘要代替运行证据 |
| 190–196 | 把 `practice.ts` 当作最终系统的可执行规格和故障预演 | 在固定 checkout 中实现、装载、测试并卸载最终插件 | 交付真实集成产物及测试/卸载证据；独立 mini-harness 单独通过不算毕业 |

第 169 晚前完成一次性环境准备：clone 官方仓库，detach 到 `47f943859bef60e4160492346772ded9b24f765a`，执行 `pnpm install --frozen-lockfile`，再以 `git rev-parse HEAD` 核对完整 SHA。169–175 必须始终复用这个 clone 内的同一 `tmp/cordis-tutorial`；每晚保存四项证据：完整 HEAD、实际命令、退出码、足以证明当晚语义的关键输出。教程统一从该目录运行 `node --import tsx ../../vendor/cordis/bin.js`，除教程明确要求的 HMR 常驻进程外都应正常退出。

本机在课程生成阶段没有 Node，因此这里只规定到学习时必须完成的运行门槛，并不声称已经执行过上述 TypeScript、pnpm 或 Harness 集成命令。

## 28 周路线

| 周 | 晚次 | 主题 | 阶段产物 |
|---:|---:|---|---|
| 01 | 001–007 | 命题逻辑与证明对象 | 命题 AST、解释器与推导检查器 |
| 02 | 008–014 | 归纳、关系、高阶函数与 fold | 关系闭包和等式推理实验 |
| 03 | 015–021 | 半群、幺半群、群、同态、自由结构、偏序 | 可执行代数定律库 |
| 04 | 022–028 | BNF、AST、绑定、替换、de Bruijn | 无捕获替换与 round-trip 测试 |
| 05 | 029–035 | 无类型 Lambda calculus | CBV/CBN 求值器与 trace |
| 06 | 036–042 | STLC 与类型安全 | 类型检查器及 progress/preservation 反例搜索 |
| 07 | 043–049 | 和/积/记录/引用/子类型 | 小型带状态语言 |
| 08 | 050–056 | 双向类型检查、统一、HM、System F、存在类型 | Algorithm W 子集 |
| 09 | 057–063 | Curry–Howard、CPS、依赖与会话类型 | 类型化工具协议状态机 |
| 10 | 064–070 | 小步/大步语义、规则归纳、求值上下文 | 可重放的推导 trace |
| 11 | 071–077 | 偏序、CPO、连续函数与最小不动点 | 含发散的指称解释器 |
| 12 | 078–084 | 上下文等价、组合性、adequacy 与完全抽象 | 操作/指称结果对照器 |
| 13 | 085–091 | Hoare 逻辑、WP、VC 与循环不变量 | 验证条件生成器 |
| 14 | 092–098 | 范畴、对偶、始末对象、积余积、CCC | 有限范畴 law checker |
| 15 | 099–105 | Curry–Howard–Lambek | STLC 到 CCC combinator 翻译 |
| 16 | 106–112 | 函子、自然变换、Yoneda、极限与幺半范畴 | naturality/Yoneda 有限模型 |
| 17 | 113–119 | 伴随与 Monad 的数学定义 | free-forgetful 伴随和 Monad law tests |
| 18 | 120–126 | 计算 Monad、代数效应与 Handler | free-effect AST 与多处理器 |
| 19 | 127–133 | Coeffect、分级效应与可撤销 effect | 依赖追踪及 disposer journal |
| 20 | 134–140 | 解释器、闭包与抽象机 | MiniPL 与 CEK/SECD trace |
| 21 | 141–147 | IR、SSA、CPS、优化正确性 | source→IR→VM 差分测试 |
| 22 | 148–154 | LLM 约束生成：LMQL、PICARD、XGrammar、JSON Schema | toy CFG/JSON constrained decoder |
| 23 | 155–161 | ReAct、Toolformer、MCP、评测协议 | 可 replay 的 mock tool agent |
| 24 | 162–168 | LLM 编程系统与 TypeScript 类型机制 | typed event/service/tool registry |
| 25 | 169–175 | Cordis 官方七章教程 | 可装卸的真实 Harness 工具插件 |
| 26 | 176–182 | Cordis 论文逐节精读 | 形式规则、关键定理和源码映射 |
| 27 | 183–189 | DeepSeek Harness 固定版本源码审计 | 启动、turn、stream、tool、log 全调用链 |
| 28 | 190–196 | 最终项目、故障注入与答辩 | 插件、性质测试、设计报告与贡献提案 |

每 7 晚完成一个可运行产物；每 28 晚回做一次不看答案的综合测试。遇到证明卡住时保留失败的证明树或最小反例，不用后一天的时间掩盖它。

## 实战语言与环境检查点

- 001–161：`practice.py`，Python 3.11+ 标准库，自包含且默认离线运行。
- 162–196：`practice.ts`，因为目标仓库本身依赖 TypeScript 的结构类型、泛型、声明合并、ESM 与项目引用；用 Python 模拟这些机制不能达到毕业目标。
- 独立练习只使用 Node 可直接擦除的 TypeScript 类型语法，安装 Node 后在任务目录执行 `node practice.ts`；这会运行断言但不做完整类型检查。进入固定 Harness checkout 后还要执行仓库自己的 `pnpm typecheck` 与相关测试。
- 在第 162 晚前安装项目所要求的 Node 版本和 Corepack 管理的 pnpm。固定快照声明 Node `^22.19.0 || >=24.0.0`、pnpm `11.7.0`。
- 进入第 169 晚前另行 clone 固定 commit；API key 只在真实模型端到端实验中需要，Cordis 教程本身可无 key 完成。

当前机器没有发现 Node/npm/pnpm，所以本次课程生成时会完整运行所有 Python 自测，并对 TypeScript 文件做结构静态检查；到达第 162 晚时必须补做 `node`/`tsc`/项目集成验收。

## 核心开放材料

- UPenn, [Software Foundations](https://softwarefoundations.cis.upenn.edu/)：逻辑、类型系统、操作语义与 Hoare 逻辑。
- Wadler 等, [Programming Language Foundations in Agda](https://plfa.inf.ed.ac.uk/)：绑定、Lambda calculus、类型安全与推断。
- Andrew Pitts, [Denotational Semantics](https://www.cl.cam.ac.uk/teaching/1112/DenotSem/dens-notes-bw.pdf)：域理论、不动点、PCF 和 adequacy。
- Emily Riehl, [Category Theory in Context](https://emilyriehl.github.io/files/context.pdf)：函子、自然变换、Yoneda、伴随和 Monad。
- Fong & Spivak, [Seven Sketches in Compositionality](https://dspivak.net/7Sketches.pdf)：组合性、偏序与幺半范畴。
- Moggi, [Notions of Computation and Monads](https://person.dibris.unige.it/moggi-eugenio/publications.html)；Pretnar, [An Introduction to Algebraic Effects and Handlers](https://www.eff-lang.org/handlers-tutorial.pdf)。
- Petricek, Orchard & Mycroft, [Coeffects](https://tomasp.net/academic/papers/coeffects/)：上下文需求的形式化。
- DeepSeek Harness 固定快照的 [架构文档](https://github.com/deepseek-ai/deepseek-harness/blob/47f943859bef60e4160492346772ded9b24f765a/docs/architecture.md) 与 [Cordis 教程](https://github.com/deepseek-ai/deepseek-harness/blob/47f943859bef60e4160492346772ded9b24f765a/docs/cordis-tutorial/index.md)。

具体任务不会只链接这些入口；每晚会进一步限定到章节、页码、标题、定义、定理、源码路径或符号。

## 毕业验收

完成第 196 晚时，应能现场完成：

- 给出半群、幺半群、范畴、函子、自然变换、伴随与 Monad 的正式定义，并验证一个错误实例为什么违反定律；
- 为一个小语言写出语法、类型规则、小步语义，说明或证明 progress/preservation；
- 比较 Monad、代数效应/Handler、Coeffect 和 Cordis 可撤销 effect 的角色；
- 从配置层追到插件树，从 inbox 追到 prompt/LLM/tool/session log，再从 log 重建模型历史；
- 实现并卸载一个 Cordis 工具插件，证明没有残留 listener/service/tool；
- 对失败、取消、权限拒绝、重复 replay 和并发到达做性质测试；
- 把一个 LLM 工业需求写成类型契约、状态机、策略边界、可观测指标和可复现实验，而不是只写 prompt。
