# 第 138 晚：CEK 抽象机

## 学习目标

- 将递归 evaluator 重写为 Control–Environment–Kontinuation 状态迁移。
- 用 continuation frame 明确求值顺序。

## 前置知识与关联任务

需要 080 的 continuation/CPS、137 的 closure 和 064 的小步语义。

## 必读材料（计入今晚 60 分钟）

| 分钟 | 材料 | 版本 | 精确范围 | 带着什么问题读 |
|---:|---|---|---|---|
| 14 | [Felleisen-style CEK notes, Northeastern PL](https://pages.github.khoury.northeastern.edu/sholtzen/cs4400-spr25/lecture-notes/lec15-abstract-machines/) | course notes 2025 | CEK state definition至 application transitions | 每个 frame 保存了 evaluator 调用栈中的哪些局部数据？ |
| 6 | [Cambridge Semantics notes](https://www.cl.cam.ac.uk/teaching/2526/Semantics/notes.pdf) | 2025–26 | evaluation contexts 段落 | context 与 continuation frame 如何对应？ |

## 精读导引

状态是 `(control,env,kont)`。遇到 `Add(a,b)` 时保存“算完左边还要算右边”的 frame；值回到 frame 决定下一步。这样调用栈变成数据，可以记录、暂停和检查。每条 transition 必须减少当前控制或推进 continuation，避免隐式递归。

## 必须完成的推导或证明

列出 `1+(2+3)` 的全部 CEK 状态，确认左到右顺序和最终空 continuation。

## 代码实战

实现 `Num/Add` CEK 机，输出 trace；检查终止态唯一、错误 frame 拒绝和步数边界。

## 与 DeepSeek Harness / LLM 工业应用的联系

Agent turn/step/inbox/cancel 也适合用显式状态机审计。CEK 训练把“控制接下来做什么”从宿主调用栈中显式化。

## 60 分钟安排

- 0–5：写 CEK 三元组。
- 5–25：精读 transition。
- 25–47：运行并打印 trace。
- 47–55：手推完整状态列。
- 55–60：验收。

## 验收标准

- trace 与手推一致。
- 终态必须 control 为值且 kont 为空。
- 能把递归 evaluator 分支映射到 frame。

## 可选延伸

加入 closure 与 application frame；不计入今晚。
