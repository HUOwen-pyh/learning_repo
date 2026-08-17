# 第183晚：Harness 启动、Profile 与 Bundle 审计

## 目标与前置

- 目标：沿 CLI dispatch→profile 解析→bundle patch 分层→Cordis 根树挂载，审计真实启动路径。
- 前置：Cordis service/effect、TypeScript class。

## 计入 60 分钟的必读

| 分钟 | 材料 | 版本 | 精确范围 | 问题 |
|---:|---|---|---|---|
| 5 | [architecture.md](https://github.com/deepseek-ai/deepseek-harness/blob/47f943859bef60e4160492346772ded9b24f765a/docs/architecture.md#L12-L30) | Harness 47f943859bef60e4160492346772ded9b24f765a | path docs/architecture.md；L12–L30；heading Profiles and bundles；checked_at 2026-08-15 | profile、bundle、patch layer 各自拥有什么？ |
| 4 | [apps/cli/src/bin.ts](https://github.com/deepseek-ai/deepseek-harness/blob/47f943859bef60e4160492346772ded9b24f765a/apps/cli/src/bin.ts#L23-L43) | 同一 commit | path apps/cli/src/bin.ts；L23–L43；symbols parseDshArgs、runProfile、runDumpConfig；checked_at 2026-08-15 | 哪些 mode 才进入 profile boot？ |
| 8 | [app-boot/profile.ts](https://github.com/deepseek-ai/deepseek-harness/blob/47f943859bef60e4160492346772ded9b24f765a/packages/boot/app-boot/src/profile.ts#L322-L396) | 同一 commit | path packages/boot/app-boot/src/profile.ts；定向读 L322–333、L335–380、L381–396；symbols resolveBundleDir、loadProfile、composeEntries；checked_at 2026-08-15 | bundle 顺序如何变成一个 entry list？ |
| 8 | [apps/cli/src/profile-boot.ts](https://github.com/deepseek-ai/deepseek-harness/blob/47f943859bef60e4160492346772ded9b24f765a/apps/cli/src/profile-boot.ts#L121-L159) | 同一 commit | path apps/cli/src/profile-boot.ts；L121–L159；symbols composeProfile、prepareProfile、resolveTelemetryPatch；checked_at 2026-08-15 | user/home/overlay/telemetry 层的优先级是什么？ |

## 阅读导引

先从 `bin.ts` 的 `profile` 分支进入，再把 `loadProfile`、`composeEntries`、`composeProfile` 连成调用图。对每层记录来源、顺序和相同 id 的覆盖结果，不再用 AgentLoop 代替 profile/bundle 审计。

## 核心推导

Profile 是有名组合，bundle 是 patch 层的分发单位。固定代码的有效顺序是 bundle 列表、profile patch、home patch、`--patch` overlay，再加 launcher 派生层；最终在空 entry list 上复用 Include 的 patch 语义。

## 工业联系与事实标签

- [THEOREM] 若各 patch 层按固定次序作确定性合成，则相同 bundle/profile/home/overlay 输入产生相同完整 config。
- [EMPIRICAL] 固定源码先按 bundle 列表组成 entries，再叠加 profile、home、命令行 overlay 与 launcher 派生层；CLI 的 `dump-config` 走同一 profile composition 路径。
- [INFERENCE] 保存 SHA、输入层及完整 dump-config，可把“实际启动了什么”变成可复核的部署证据。
- [OPEN] boot 取得部分 context 后失败时，进程内 disposer 可回收已挂载资源；进程崩溃仍需外部监督与持久化恢复协议。

## 严格 60 分钟

- 0–5：核对 `git rev-parse HEAD` 为固定 SHA；5–30：按表追踪启动路径；30–40：用 `practice.ts` 预检 layer precedence；40–55：在真实 checkout 运行 `pnpm dsh --profile headless --dump-config`，将输出行标回 bundle/profile 来源；55–60：保存命令、SHA 和层次图。

## 验收

同时提交：`practice.ts` 预检结果、固定 SHA checkout 的 dump-config 输出、一张标明 `bin.ts→loadProfile→composeEntries→runProfile` 的路径图；任一缺失则本晚未完成。

## 可选延伸

阅读 examples/headless-agent/cordis.yml 固定提交版本，不计时。
