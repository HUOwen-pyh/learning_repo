# 第153晚：JSON Schema 词汇与验证

## 目标与前置

- 目标：理解 Core、Validation、词汇表、annotation 与 assertion 的分工。
- 前置：JSON、递归数据、布尔逻辑。

## 计入 60 分钟的必读

| 分钟 | 材料 | 版本 | 精确范围 | 问题 |
|---:|---|---|---|---|
| 10 | [JSON Schema Core](https://json-schema.org/draft/2020-12/json-schema-core.html) | Draft 2020-12, 2022-06-16 | §§4、6、8 | dialect 与 vocabulary 如何声明？ |
| 10 | [JSON Schema Validation](https://json-schema.org/draft/2020-12/json-schema-validation) | Draft 2020-12 | §§3、6.1、6.5 | assertion 与 annotation 有何不同？ |

## 阅读导引

只追踪 type、required、properties、items 四个关键字。写下它们作用的数据实例位置，避免把 schema 本身与被验证实例混淆。

## 核心推导

验证可定义为递归关系 V(schema, instance, location)。type 在当前位置断言类型；required 断言对象键集合；properties 把子 schema 递归应用到相应值；items 对数组元素逐一递归。错误路径是语义输出的一部分。

## 工业联系与事实标签

- [THEOREM] 对本晚有限、无引用的 schema 子集，结构递归验证必然终止。
- [EMPIRICAL] Draft 2020-12 是所链接规范版本；具体模型的 schema 支持通常只是该规范子集。
- [INFERENCE] 错误携带实例路径比单一布尔值更适合工具调用诊断。
- [OPEN] 不同厂商结构化输出对完整规范关键字的支持随版本变化，必须实测。

## 严格 60 分钟

- 0–5：写一份工具参数 schema；5–25：必读；25–48：运行验证器；48–55：增加 minimum；55–60：解释错误路径。

## 验收

对象、数组、缺键、空数组边界断言通过；能指出实现未覆盖哪些规范。

## 可选延伸

阅读 Core §10 applicator vocabulary，不计时。
