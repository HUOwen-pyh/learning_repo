# 第 129 晚：Indexed Comonad 与 Coeffect 语义

## 学习目标

- 理解 coeffect 语义为什么常用 indexed comonad，而不是普通 Reader Monad。
- 写出上下文抽取和扩展操作的有限实例。

## 前置知识与关联任务

需要 106–112 的函子/自然变换、119 的 Monad 和 127–128 的 coeffect。

## 必读材料（计入今晚 60 分钟）

| 分钟 | 材料 | 版本 | 精确范围 | 带着什么问题读 |
|---:|---|---|---|---|
| 16 | [Coeffects](https://tomasp.net/academic/papers/coeffects/) | ICALP 2014 | 论文 §3 “Semantics”，indexed comonad 定义及 context-dependent 例 | 索引记录了什么资源/上下文信息？ |
| 4 | 同文 | ICALP 2014 | §3 中 counit/coextension 对应段 | extract 与 duplicate/coextend 的方向为何和 Monad 相反？ |

## 精读导引

Monad 从值产生计算并用 bind 串接；Comonad 从带上下文的值提取焦点，并让局部计算在扩展上下文上运行。Indexed 版本让输入/输出上下文需求进入类型。今天用有限窗口模拟，不试图在 Python 动态类型中完整编码论文的索引证明。

## 必须完成的推导或证明

为长度为奇数的窗口写 `extract` 和 `extend`，验证 `extend(extract)=id` 的有限实例；说明边界处理属于何种额外语义选择。

## 代码实战

实现一维上下文窗口 comonad 玩具，计算邻域平均；检查恒等律并用偶数窗口构造无中心反例。

## 与 DeepSeek Harness / LLM 工业应用的联系

prompt/context 注入可视为依赖周围环境的计算，但 Harness 的 inbox、logged visibility 和 service context 各有具体规则。Comonad 是解释工具，不是替代源码审计。

## 60 分钟安排

- 0–5：对比 Monad/Comonad 箭头。
- 5–25：精读 indexed semantics。
- 25–45：运行窗口实验。
- 45–55：验证 counit law 与边界反例。
- 55–60：验收。

## 验收标准

- 能说出 index 表示的上下文需求。
- 窗口 extract/extend 正例通过，偶数窗口失败。
- 不把 Reader Monad 与 Coeffect 简单等同。

## 可选延伸

研究 store comonad；不计入今晚。
