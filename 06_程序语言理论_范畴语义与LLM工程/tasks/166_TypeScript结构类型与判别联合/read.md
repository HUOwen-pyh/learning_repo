# 第166晚：TypeScript 结构类型与判别联合

## 目标与前置

- 目标：用结构类型描述插件契约，用判别联合封闭 `AgentEvent`，并做穷尽检查，同时避开 DOM 全局 `Event` 名称冲突。
- 前置：静态类型、联合类型、switch。

## 计入 60 分钟的必读

| 分钟 | 材料 | 版本 | 精确范围 | 问题 |
|---:|---|---|---|---|
| 9 | [Type Compatibility](https://www.typescriptlang.org/docs/handbook/type-compatibility.html) | checked_at 2026-08-15 | Starting out、Comparing two functions、Unsoundness note | 结构兼容为何允许额外字段？ |
| 11 | [Narrowing](https://www.typescriptlang.org/docs/handbook/2/narrowing.html#discriminated-unions) | checked_at 2026-08-15 | Discriminated unions、never exhaustiveness | kind 字段怎样缩窄 payload？ |

## 阅读导引

先比较 nominal 与 structural，再为模块内的 `AgentEvent` 设计稳定 kind。不要在无模块边界的脚本中声明全局 `Event`，因为浏览器的 DOM 库已定义同名接口。把 default 分支赋给 never，观察新增事件而漏改消费者时的编译失败。

## 核心推导

结构子类型按所需成员判断；对象拥有更多成员仍可满足较小接口。判别联合 U=A|B 中检查 kind 后，控制流分析把变量缩窄到对应成员；剩余分支应为 never。

## 工业联系与事实标签

- [THEOREM] 在 TypeScript 编译器规则内，never 赋值可作为封闭联合穷尽性静态检查。
- [EMPIRICAL] TypeScript 官方文档明确说明其类型系统存在刻意的不健全取舍。
- [INFERENCE] 外部 JSON 必须先做运行时验证，不能由类型断言制造信任；领域事件也应采用模块化名称，避免声明合并或全局冲突。
- [OPEN] 大型插件生态中开放扩展与封闭穷尽联合天然张力仍需分层设计。

## 严格 60 分钟

- 0–5：写 union；5–25：必读；25–48：运行事件 reducer；48–55：新增 cancel 事件并改全分支；55–60：解释静态/运行时边界。

## 验收

三类事件、非法运行时事件、空文本边界断言；理解 extra property 与 excess property check 差异。

## 可选延伸

阅读 Handbook Excess Property Checks，不计时。
