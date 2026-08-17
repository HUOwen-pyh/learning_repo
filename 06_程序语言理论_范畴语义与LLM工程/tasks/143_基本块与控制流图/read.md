# 第 143 晚：基本块与控制流图

## 学习目标

- 将跳转指令切分为基本块并建立 CFG。
- 检查入口可达性、终结指令和边目标不变量。

## 前置知识与关联任务

需要 009 的图、027 的状态机和 141–142 的 IR。

## 必读材料（计入今晚 60 分钟）

| 分钟 | 材料 | 版本 | 精确范围 | 带着什么问题读 |
|---:|---|---|---|---|
| 14 | [LLVM Kaleidoscope Ch.5](https://llvm.org/docs/tutorial/MyFirstLanguageFrontend/LangImpl05.html) | LLVM current | “If/Then/Else”至 PHI 前的 basic block/control flow 构造 | 哪些指令结束基本块，边在哪里产生？ |
| 6 | [LLVM Language Reference](https://llvm.org/docs/LangRef.html#terminator-instructions) | LLVM current | Terminator Instructions 开头及 `br` | 一个基本块为什么必须恰有一个 terminator？ |

## 精读导引

Leader 是入口、跳转目标或 terminator 后首指令。基本块内部单入口、除末尾外无跳转；CFG 边由 terminator 决定。不可达块不一定非法，但必须显式报告，避免测试遗漏死代码。

## 必须完成的推导或证明

把一个 if/else 字节码切成四块，写出邻接表和支配直觉；构造跳转到不存在 label 的反例。

## 代码实战

解析带 label/JUMP/JZ/RET 的 toy IR，建 CFG、求可达块并验证每块 terminator。

## 与 DeepSeek Harness / LLM 工业应用的联系

agent turn/tool pipeline 同样可画控制流图；拒绝、取消和 retry 边若漏画，测试就不会覆盖完整状态空间。

## 60 分钟安排

- 0–5：列 leader 规则。
- 5–25：精读 CFG/terminator。
- 25–47：运行构图器。
- 47–55：手画 if/else 和坏 label。
- 55–60：验收。

## 验收标准

- 切块和边准确。
- 缺 terminator/未知目标被拒绝。
- 输出不可达块集合。

## 可选延伸

计算 dominator；不计入今晚。
