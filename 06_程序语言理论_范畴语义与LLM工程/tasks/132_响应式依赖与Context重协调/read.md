# 第 132 晚：响应式依赖与 Context 重协调

## 学习目标

- 模拟 provider 增删时依赖插件的激活、停用和重新激活。
- 分开 spatial dependency 与 temporal disposer 顺序。

## 前置知识与关联任务

需要 127–128 的 context requirements 和 131 的可撤销 effect。

## 必读材料（计入今晚 60 分钟）

| 分钟 | 材料 | 版本 | 精确范围 | 带着什么问题读 |
|---:|---|---|---|---|
| 11 | [Cordis Primer](https://github.com/deepseek-ai/deepseek-harness/blob/47f943859bef60e4160492346772ded9b24f765a/docs/cordis-primer.md) | `47f943…` | Context、inject、Loader Configuration 三段 | 依赖何时求值，provider 消失后谁负责停用？ |
| 9 | [Architecture](https://github.com/deepseek-ai/deepseek-harness/blob/47f943859bef60e4160492346772ded9b24f765a/docs/architecture.md) | `47f943…` | Profiles and bundles 中 layer/patch 顺序 | 配置变化如何改变插件树而不手写启动序列？ |

## 精读导引

插件声明需求，而不是假设人工加载顺序。协调器在需求满足时挂载，在需求失效时先撤销其 effects。Provider 恢复后可重新挂载。配置 overlay 还有明确优先级；依赖集合与配置覆盖是两套规则。

## 必须完成的推导或证明

画 `credentials→http→search-tool` 依赖链；删除 `credentials` 后列出安全停用顺序，再恢复并列出挂载顺序。

## 代码实战

实现有持久状态的小型 reactive resolver：逐个处理 provider `add/remove` 事件，需求满足时按拓扑序发出 `mount`，需求失效时按逆拓扑序发出 `unmount`。每个事件后检查“active 插件的需求已满足”，而不是每次从一个 `base` 集合重新求闭包。

## 与 DeepSeek Harness / LLM 工业应用的联系

这是 Cordis spatial composability 的工程轮廓（FACT）。真实实现还包含 fiber、isolate realm、配置表达式与 HMR，后续固定源码任务再读。

## 60 分钟安排

- 0–5：画依赖链。
- 5–25：精读固定文档。
- 25–47：运行 resolver 事件序列。
- 47–55：证明每步 active invariant。
- 55–60：验收。

## 验收标准

- provider 删除后没有悬空 active consumer。
- 重加后按依赖恢复；事件日志明确显示卸载逆拓扑、挂载拓扑顺序。
- 能区分依赖解析和 overlay precedence。

## 可选延伸

阅读 Cordis tutorial 第6章；不计入今晚。
