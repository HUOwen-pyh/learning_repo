# 第 127 晚：Effect 与 Coeffect 的边界

## 学习目标

- 区分计算对外部世界产生什么 effect 与计算从上下文需要什么 coeffect。
- 为同一表达式分别写 effect 注记和上下文需求注记。

## 前置知识与关联任务

回顾 120–126 的计算 effect，以及 077 的 reader/context 需求。

## 必读材料（计入今晚 60 分钟）

| 分钟 | 材料 | 版本 | 精确范围 | 带着什么问题读 |
|---:|---|---|---|---|
| 14 | [Petricek–Orchard–Mycroft, Coeffects](https://tomasp.net/academic/papers/coeffects/) | ICALP 2014 author page | 论文 §1 Introduction，effect/coeffect 对照图及例子 | 输入上下文需求为什么不能只写在输出 effect 上？ |
| 6 | [Cordis Primer](https://github.com/deepseek-ai/deepseek-harness/blob/47f943859bef60e4160492346772ded9b24f765a/docs/cordis-primer.md) | commit `47f943…` | “Cordis In Five Ideas”中的 context、inject 两项 | 插件声明依赖与运行后产生注册分别属于哪一侧？ |

## 精读导引

effect 描述计算可能做的事，如写状态、抛错、调用工具；coeffect 描述计算对上下文的要求，如需要某服务、可使用变量多少次、需要邻域数据。两者可以同时存在。Cordis 的 `inject` 是依赖需求的工程机制，论文中的 coeffect 是更形式化的上下文注记，不应只按名字认定完全等价。

## 必须完成的推导或证明

为“读取凭证服务并发出网络请求”分别列出 required context 与 produced effects；删除任一注记后构造一个误判。

## 代码实战

实现 `requires/provides/declared_effects` 静态检查与实际执行 trace 的动态核对；必须检查 `set(actual_trace) ⊆ declared_effects`，并用“恰好等于/真子集可接受、越界集合拒绝”覆盖边界。

## 与 DeepSeek Harness / LLM 工业应用的联系

插件通过 `inject` 等待服务存在，挂载后再注册 listener/tool/service。把需求与产出分开是理解 Cordis 空间/时间组合性的第一步。

## 60 分钟安排

- 0–5：各写三个 effect/coeffect 例子。
- 5–25：精读论文导言与固定 primer。
- 25–46：运行依赖/effect 检查器。
- 46–55：完成网络例与误判。
- 55–60：验收。

## 验收标准

- 不用“输入/输出”口号含混替代正式需求。
- 缺依赖和实际 trace 中的未声明 effect 均被拒绝，真子集不会被误拒。
- 能说明课程模型与 Cordis 机制的证据边界。

## 可选延伸

阅读 coeffects 论文 §2；不计入今晚。
