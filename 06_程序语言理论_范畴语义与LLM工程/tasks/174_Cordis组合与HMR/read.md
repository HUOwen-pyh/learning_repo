# 第174晚：Cordis 教程 6——组合与 HMR

## 目标与前置

- 目标：理解稳定 id、plugin tree diff、isolate、HMR 与 PENDING 诊断。
- 前置：第169–173晚、树差分。

## 计入 60 分钟的必读

| 分钟 | 材料 | 版本 | 精确范围 | 问题 |
|---:|---|---|---|---|
| 20 | [Composition and HMR](https://github.com/deepseek-ai/deepseek-harness/blob/47f943859bef60e4160492346772ded9b24f765a/docs/cordis-tutorial/06-composition-and-hmr.md#L1-L113) | Harness 47f943859bef60e4160492346772ded9b24f765a | path docs/cordis-tutorial/06-composition-and-hmr.md；全章 L1–L113；symbols id、disabled、isolate、FiberState.PENDING；checked_at 2026-08-15 | 无稳定 id 为何造成无关 remount？ |

## 阅读导引

把旧/新配置按 id 做映射：同 id 同内容保留，同 id 改内容重配，删除卸载，新增挂载。`disabled` 表示「配置仍存在，但期望状态不挂载」：enabled→disabled 是 remove，disabled→enabled 是 add，而新增的 disabled entry 不应 add。注意 PENDING 是合法状态，诊断必须列出缺失能力。

## 核心推导

稳定 identity 将配置 diff 从按位置比较转为按键比较。若每次读取都生成新 id，即使内容相同也被解释为 delete+add，导致 effect 不必要地展开和重建。

## 工业联系与事实标签

- [THEOREM] 唯一稳定键可把两个有限 entry 集合的对应关系定义为键相等。
- [EMPIRICAL] 教程说明 HMR 依赖 logger 与 timer 服务，缺失时相关插件可能处于 PENDING。
- [INFERENCE] 生产诊断应显示“谁等待哪个服务”，而非仅显示未启动。
- [OPEN] 外部连接无缝迁移通常超出普通模块 HMR 的保证。

## 真实固定 checkout 实战

继续使用同一教程工作区。按官方第六章给 logger、timer、hmr 与第 169 晚的 `hello.ts` 配置稳定 `id`；在 `hello.ts` 中加入一个只打印 marker 的 `ctx.effect` disposer。运行真实 launcher 后修改并保存 `hello.ts`，证据应同时出现 HMR reload、旧实例 disposer marker 与新实例输出。随后按章运行 PENDING 诊断：让 `needs-timer` 缺少 timer 时打印诊断，再恢复 timer 并观察其加载。用 Ctrl-C 停止常驻 watcher，并记录正常清理/停止。

## 严格 60 分钟

- 0–5：闭卷画按稳定 id 对齐的 tree diff。
- 5–25：精读固定提交第六章 L1–L113。
- 25–37：运行本地 `practice.ts`，检查 keep/add/remove/replace/disabled 边界。
- 37–43：在连续教程工作区按章配置 logger、timer、hmr、hello，并给 hello 加 disposer marker。
- 43–49：启动真实 launcher、保存一次文件编辑，记录 reload、卸载 marker 与新实例输出。
- 49–55：运行章内 PENDING 诊断的缺/有 timer 对照，并用 Ctrl-C 停止 watcher。
- 55–60：核对双门证据并写三句复盘。

## 验收

- 本地门：keep/add/remove/replace/disabled 边界断言通过，并能解释 isolate。
- 真实门：固定 HEAD、HMR reload、旧实例 disposer、新实例输出、缺 timer 的 PENDING 与恢复 timer 后加载的证据齐全；常驻 watcher 已停止。
- 两门必须同时通过；只有纯函数 tree diff 输出不算完成真实 HMR。

## 可选延伸

加入嵌套 group 路径，不计时。
