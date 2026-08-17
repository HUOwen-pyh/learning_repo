# 第 144 晚：SSA 与 Φ 节点

## 学习目标

- 解释静态单赋值和控制流汇合处 Φ 的语义。
- 检查 Φ 的 incoming label 与 CFG 前驱一致。

## 前置知识与关联任务

需要 143 的基本块/CFG 和 047–052 的和类型/控制分支。

## 必读材料（计入今晚 60 分钟）

| 分钟 | 材料 | 版本 | 精确范围 | 带着什么问题读 |
|---:|---|---|---|---|
| 14 | [LLVM Kaleidoscope Ch.5](https://llvm.org/docs/tutorial/MyFirstLanguageFrontend/LangImpl05.html) | LLVM current | “PHI Node”从创建至 incoming blocks 完成 | Φ 选择的是布尔条件还是实际前驱边？ |
| 6 | [LLVM LangRef: phi](https://llvm.org/docs/LangRef.html#phi-instruction) | LLVM current | `phi` syntax/semantics 全段 | Φ 为什么必须位于块开头？ |

## 精读导引

SSA 中变量只定义一次；if 两支产生 `x_then,x_else`，join 用 `x=phi[(x_then,then),(x_else,else)]`。选择取决于控制从哪个 predecessor 来，不是重新计算条件。每个前驱必须恰有一个 incoming。

## 必须完成的推导或证明

把命令式 `if c then x=1 else x=2; y=x+3` 转成 SSA，列 def-use 和 Φ 前驱映射。

## 代码实战

实现 Φ evaluator/verifier，测试两条边、缺 incoming、额外 incoming 和未知 predecessor。

## 与 DeepSeek Harness / LLM 工业应用的联系

并发或分支后的状态合并必须保留“来自哪条路径”。仅合并最终值会丢失审批/错误来源；Φ 提供控制敏感合并的最小模型。

## 60 分钟安排

- 0–5：写 SSA 定义。
- 5–25：精读 Φ。
- 25–45：运行 verifier。
- 45–55：完成命令式转 SSA。
- 55–60：验收。

## 验收标准

- incoming 与 predecessor 一一对应。
- 四类正反测试通过。
- 能说明 Φ 不重新判断条件。

## 可选延伸

研究 dominance frontier；不计入今晚。
