# 第 139 晚：SECD 的 Stack–Environment–Control–Dump

## 学习目标

- 说明 SECD 四个组件及函数调用时 dump 的作用。
- 比较基于语法控制的 CEK 与基于指令控制的 SECD。

## 前置知识与关联任务

需要 137 的 closure、138 的抽象机和 142 将学习的字节码概念。

## 必读材料（计入今晚 60 分钟）

| 分钟 | 材料 | 版本 | 精确范围 | 带着什么问题读 |
|---:|---|---|---|---|
| 12 | [Landin, The Mechanical Evaluation of Expressions](https://academic.oup.com/comjnl/article-pdf/6/4/308/1067901/6-4-308.pdf) | *The Computer Journal* 6(4), 1964 | 论文页 308–320；今晚精读 pp. 313–314 中对 S/E/C/D、`ap` 与函数返回的机器描述 | `ap` 把调用者的哪些状态放进 dump，返回时怎样恢复？ |
| 8 | [Cambridge, Foundations of Functional Programming](https://www.cl.cam.ac.uk/teaching/2006/FFuncProg/fofp.pdf) | University of Cambridge, Lent 2007 | 讲义标注页 97–100：“The SECD Machine”与“state transitions”，重点 closure 规则和应用规则 | closure 为什么必须携带定义处环境？dump frame 里是哪三个分量？ |

## 精读导引

先用 Cambridge 讲义的状态框逐条抄写转换，再回到 Landin 原文核对术语。Stack 保存中间值，Environment 保存变量，Control 保存待执行指令，Dump 保存调用返回点；应用时保存调用者的 `(S,E,C)`，返回时恢复。今天实现算术子集，无函数时 dump 为空；随后用一次手工 CALL/RET 演示 dump。不要把宿主 Python 栈当作 SECD dump。

## 必须完成的推导或证明

为后缀代码 `1 2 3 + +` 列出 S/E/C/D；说明每步 stack height 的变化不变量。

## 代码实战

实现 `CONST/ADD` SECD 子集，检测 stack underflow 和终态剩余多值；输出可 replay trace。

## 与 DeepSeek Harness / LLM 工业应用的联系

显式控制与返回点便于暂停、恢复和序列化；Harness 的 durable session log 不等同机器 dump，但同样避免把所有控制状态藏在调用栈。

## 60 分钟安排

- 0–5：写 SECD 四字母。
- 5–25：精读机器组件。
- 25–46：运行字节码机。
- 46–55：手推状态和 height 不变量。
- 55–60：验收。

## 验收标准

- 四组件职责准确。
- 正常/underflow/多值终态测试通过。
- trace 可由初态确定性重放。

## 可选延伸

加入 closure、AP 与 RTN；不计入今晚。
