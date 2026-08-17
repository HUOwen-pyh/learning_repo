# 第 040 晚：弱化、重命名与替换引理

## 学习目标

- 陈述 weakening 与 substitution preserves typing。
- 解释 binder case 为什么扩展上下文映射。
- 用类型检查器验证一组 lemma 实例。

## 前置任务

- 第 026 晚“捕获规避替换”。
- 第 037 晚“算法型类型检查”。

## 必读材料（计入今晚 60 分钟）

| 分钟 | 材料 | 版本 | 精确范围 | 带着问题读 |
|---:|---|---|---|---|
| 14 | [PLFA — Properties](https://plfa.github.io/22.08/Properties/) | 22.08 | “Prelude to preservation” 三步 programme | preservation 的 β case 缺哪条 lemma？ |
| 14 | [PLFA — Properties](https://plfa.github.io/22.08/Properties/) | 22.08 | “Renaming” 至 `weaken` corollary；随后 Substitution 的 theorem statement 与前三个 cases | 进入 lambda 时上下文和替换映射怎样变化？ |

## 精读导引

弱化是“加入未用假设不破坏已有推导”。替换引理把两个推导拼起来：`Γ,x:A⊢t:B` 与 `Γ⊢s:A` 推出 `Γ⊢t[x:=s]:B`。它正对应 β 后类型仍在。

## 必须完成的推导

1. 写出 weakening 和 substitution 的量词化陈述。
2. 对 variable case 分 `y=x` 与 `y≠x`。
3. 对 abstraction case说明遮蔽与必要的 α/闭项条件。

结论类型：【基础引理】替换与 typing 可交换，是 preservation 的关键组合律。

## 与 DeepSeek Harness / LLM 工业应用的联系

基础联系：把一个经 schema 验证的工具结果代入后续模板，应保持后续节点的接口类型。该类“局部验证可组合”是流水线可靠性的核心，但外部语义真实性仍需单独检查。

## 60 分钟安排

| 环节 | 分钟 |
|---|---:|
| 必读材料 | 28 |
| 三个 proof cases | 12 |
| 完成 lemma 实例检查 | 16 |
| 验收 | 4 |
| **合计** | **60** |

## 验收标准

- 两条 lemma 的上下文与类型下标完整。
- 正确替换保持类型，错类型替换被拒绝。
- shadowing 边界不替换 binder 内同名变量。

## 可选延伸

- 对 typing derivation 实现真正的 `substitution_proof` 转换，而非重新 infer。

