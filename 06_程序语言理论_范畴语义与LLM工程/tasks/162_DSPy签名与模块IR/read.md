# 第162晚：DSPy 签名与模块 IR

## 目标与前置

- 目标：把提示程序表示为 signature、module 与可组合的中间表示，而非手写长提示。
- 前置：函数签名、AST、纯函数组合。

## 计入 60 分钟的必读

| 分钟 | 材料 | 版本 | 精确范围 | 问题 |
|---:|---|---|---|---|
| 12 | [DSPy: Compiling Declarative Language Model Calls into Self-Improving Pipelines](https://proceedings.iclr.cc/paper_files/paper/2024/file/f1cf02ce09757f57c3b93c0db83181e0-Paper-Conference.pdf) | ICLR 2024 | §1–§2 | 声明式 signature 隐藏了什么实现选择？ |
| 8 | 同上 | 同版 | §3.1 Programming Model | module 与一次模型调用为何不同？ |

## 阅读导引

将输入字段、输出字段、字段说明、模块组合分别画成 IR 节点。注意 signature 描述任务契约，prompt/demo/model 参数是可编译实现。

## 核心推导

设签名 σ: I→O，模块 M 实现 σ。串联 M1:I→A 与 M2:A→O 得到 M2∘M1:I→O；字段映射是组合成立的接口证明。运行时仍需验证不可信模型输出。

## 工业联系与事实标签

- [THEOREM] 类型匹配的函数组合保持输入输出接口。
- [EMPIRICAL] DSPy 论文的改进结果来自指定任务、模型、metric 与 optimizer 配置。
- [INFERENCE] 稳定 IR 能把业务契约从模型供应商 prompt 细节中隔离。
- [OPEN] 自然语言字段描述无法单独保证输出语义正确。

## 严格 60 分钟

- 0–5：写签名；5–25：必读；25–48：运行 IR；48–55：增加字段映射失败；55–60：说明声明与实现分离。

## 验收

串联、缺字段、空管线断言通过；能给 IR 节点定义不变量。

## 可选延伸

阅读论文 §3.2 的 teleprompter 概念，不计时。
