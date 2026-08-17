# 第167晚：TypeScript 泛型、条件映射与声明合并

## 目标与前置

- 目标：用泛型关系、条件类型、映射类型和开放接口建立类型化服务表。
- 前置：第166晚、keyof、索引访问类型。

## 计入 60 分钟的必读

| 分钟 | 材料 | 版本 | 精确范围 | 问题 |
|---:|---|---|---|---|
| 6 | [Generics](https://www.typescriptlang.org/docs/handbook/2/generics.html) | checked_at 2026-08-15 | Generic Constraints、Using Type Parameters in Generic Constraints | K extends keyof T 保证什么？ |
| 5 | [Conditional Types](https://www.typescriptlang.org/docs/handbook/2/conditional-types.html) | checked_at 2026-08-15 | Constraints、Inferring Within Conditional Types | infer 在何处绑定？ |
| 5 | [Mapped Types](https://www.typescriptlang.org/docs/handbook/2/mapped-types.html) | checked_at 2026-08-15 | Mapping Modifiers、Key Remapping | 如何由服务表导出 getter？ |
| 4 | [Declaration Merging](https://www.typescriptlang.org/docs/handbook/declaration-merging.html) | checked_at 2026-08-15 | Merging Interfaces、Module Augmentation | 插件怎样扩开放表？ |

## 阅读导引

用 ServiceMap 做唯一真相源；get<K extends keyof ServiceMap> 返回 ServiceMap[K]，防止服务名与返回值失去关联。理解声明合并是编译期开放世界，不会自动注册运行时值。

## 核心推导

泛型依赖保持键值相关性；若写 get(name:string):unknown，这一关系消失。映射类型可从一张表机械导出只读、可选或 getter 形状，减少重复契约漂移。

## 工业联系与事实标签

- [THEOREM] 对 K extends keyof T，索引访问 T[K] 只可能选择 T 声明的键对应类型。
- [EMPIRICAL] 类型擦除后运行时无 ServiceMap，必须有真实 registry 与验证。
- [INFERENCE] Harness/Cordis 式插件可用 module augmentation 扩编译期服务目录。
- [OPEN] 第三方声明冲突、版本偏差和重复标识仍需包管理约束。

## 严格 60 分钟

- 0–5：写 ServiceMap；5–25：必读；25–48：运行 registry；48–55：增加 logger 服务；55–60：解释类型擦除。

## 验收

两服务、缺失服务、空字符串边界断言；能写 get<K extends keyof T>。

## 可选延伸

研究 satisfies 运算符，不计时。
