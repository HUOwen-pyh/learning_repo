# 第173晚：Cordis 教程 5——配置验证

## 目标与前置

- 目标：理解 Config schema、默认值、变更触发的重新配置与失败回滚边界。
- 前置：JSON Schema、第170晚。

## 计入 60 分钟的必读

| 分钟 | 材料 | 版本 | 精确范围 | 问题 |
|---:|---|---|---|---|
| 20 | [Config](https://github.com/deepseek-ai/deepseek-harness/blob/47f943859bef60e4160492346772ded9b24f765a/docs/cordis-tutorial/05-config.md#L1-L100) | Harness 47f943859bef60e4160492346772ded9b24f765a | path docs/cordis-tutorial/05-config.md；章内 Config schema、defaults、validation、reload；L1–L100；symbols Config、schema、apply；checked_at 2026-08-15 | config 在进入 apply 前应满足什么？ |

## 阅读导引

跟踪 raw YAML→解析对象→schema 默认/校验→typed config→apply。把 config 错误视作插件 FAILED，而非用默认值吞掉所有错误。

## 核心推导

validator V:unknown→Either<Errors,Config> 是信任边界。defaults 只补缺失值，不能修复类型错误。本晚的原子重配置模型先验证新值，再尝试完整构造新实例；验证或新实例构造失败时保留旧实例，只有成功后才 dispose 旧实例并切换。这一保证依赖「start 要么返回完整实例，要么无副作用地失败」与旧 disposer 不抛错的收窄假设；真实外部资源需要 staging 或补偿，具体 loader 策略须以源码为准。

## 工业联系与事实标签

- [THEOREM] 对有限无递归的本晚 schema，结构验证终止。
- [EMPIRICAL] 固定教程给出的 Config 机制属于该 Harness/Cordis 提交。
- [INFERENCE] 配置版本与迁移函数应进入可审计发布物。
- [OPEN] 热重载是否原子取决于 loader、外部资源和 disposer 行为。

## 真实固定 checkout 实战

继续使用同一教程工作区，按官方第五章创建带 `Config`/`schema` 的插件和相应 `cordis.yml`。先运行合法配置并记录默认值/规范化后的可见行为，再把一个字段改成章内 schema 不接受的类型并重跑，保存 Cordis 的 validation failure 与非成功路径；恢复合法配置。不要把本地 `AtomicSlot` 的“先建新实例再释放旧实例”收窄模型误写成真实 Loader 已承诺的事务语义。

## 严格 60 分钟

- 0–5：闭卷写出 raw→validate/default→typed config→apply。
- 5–25：精读固定提交第五章 L1–L100。
- 25–37：运行本地 `practice.ts`，检查类型错误、默认值、错误路径和 start 失败保留旧实例。
- 37–44：在连续教程工作区按章创建真实 Config schema、插件与合法 YAML。
- 44–50：运行真实 launcher，保存合法配置行为、默认值证据与退出码。
- 50–55：注入章内可复现的类型错误，保存 validation failure 后恢复合法配置。
- 55–60：核对双门证据并写三句复盘。

## 验收

- 本地门：合法、类型错误、缺失默认、零值边界、错误路径、无效新配置与 start 失败断言全部通过。
- 真实门：固定 HEAD 下合法 YAML 的输出、默认值证据、无效类型的 Cordis validation failure 以及恢复后的成功运行记录齐全。
- 两门必须同时通过；验收陈述须区分本地原子模型的假设和真实 Loader 实际观察到的行为。

## 可选延伸

增加 configVersion 和迁移，不计时。
