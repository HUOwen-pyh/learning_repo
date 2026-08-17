# 第171晚：Cordis 教程 3——服务与 inject

## 目标与前置

- 目标：理解 Service 注册、声明合并、硬依赖 pending 与提供者替换。
- 前置：第167、170晚。

## 计入 60 分钟的必读

| 分钟 | 材料 | 版本 | 精确范围 | 问题 |
|---:|---|---|---|---|
| 20 | [Services](https://github.com/deepseek-ai/deepseek-harness/blob/47f943859bef60e4160492346772ded9b24f765a/docs/cordis-tutorial/03-services.md#L1-L98) | Harness 47f943859bef60e4160492346772ded9b24f765a | path docs/cordis-tutorial/03-services.md；全章 L1–L98；symbols Service、inject、ctx.get；checked_at 2026-08-15 | 服务消失后 consumer 为何必须卸载并等待？ |

## 阅读导引

分别标注 runtime registration 与 compile-time declaration merging。跟踪 provider 出现、consumer 激活、provider 消失、consumer 清理、provider 重现五步。

## 核心推导

plugin 的所需集合 R 与当前服务集合 S 满足 R⊆S 时才能 ACTIVE。服务撤销使条件失真，依赖插件须卸载；服务重现后可重新 apply，避免持有陈旧引用。

## 工业联系与事实标签

- [THEOREM] R⊆S 是有限集合上可判定的激活条件。
- [EMPIRICAL] 固定教程说明 inject 是持续追踪依赖而非一次性启动检查。
- [INFERENCE] 以能力名依赖而非导入 provider，可支持 mock、沙箱与部署替换。
- [OPEN] 扁平服务命名空间下的跨组织命名治理需要额外约定。

## 真实固定 checkout 实战

继续使用同一教程工作区。按官方第三章创建 `greeter.ts` 与 `consumer.ts`，让 `cordis.yml` 同时装载二者；运行真实 launcher，交换两条 entry 后再运行，两个次序都必须输出 `Hello, world!`。再暂时移除 provider，只保留 consumer：命令应退出 0 且没有问候输出，说明 consumer 是 PENDING 而非按 YAML 顺序侥幸启动。最后恢复两个稳定 entry，供后续章节复用。

## 严格 60 分钟

- 0–5：闭卷写出激活条件 R⊆S。
- 5–25：精读固定提交第三章 L1–L98。
- 25–37：运行本地 `practice.ts`，检查等待、激活、撤销、恢复与空依赖。
- 37–43：在连续教程工作区按章创建 provider、consumer 与组合配置。
- 43–50：交换 YAML 顺序各运行一次真实 launcher，保存两次问候输出与退出码。
- 50–55：移除 provider 再运行，记录退出 0 且无问候，然后恢复配置。
- 55–60：核对双门证据并写三句复盘。

## 验收

- 本地门：等待、激活、撤销、恢复、空依赖断言全部通过。
- 真实门：固定 HEAD、两种 entry 顺序、两次 `Hello, world!`、缺 provider 时退出 0 且无问候的记录齐全；真实教程文件仍位于同一工作区。
- 两门必须同时通过；不能用“理解 inject”替代 provider 缺失实验。

## 可选延伸

为服务加入版本约束，不计时。
