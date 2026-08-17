# 第169晚：Cordis 教程 1——首个插件

## 目标与前置

- 目标：理解 apply(ctx)、三种插件形状和由配置组合应用的入口。
- 前置：TypeScript 函数/类、依赖注入概念。

## 计入 60 分钟的必读

| 分钟 | 材料 | 版本 | 精确范围 | 问题 |
|---:|---|---|---|---|
| 20 | [Your first plugin](https://github.com/deepseek-ai/deepseek-harness/blob/47f943859bef60e4160492346772ded9b24f765a/docs/cordis-tutorial/01-first-plugin.md#L1-L95) | Harness 47f943859bef60e4160492346772ded9b24f765a | path docs/cordis-tutorial/01-first-plugin.md；全章 L1–L95；symbols apply、Context；checked_at 2026-08-15 | 配置顺序为何不保证加载顺序？ |

## 阅读导引

逐个标出 function、object、Service class 三种 plugin shape。注意插件只描述贡献，launcher 和 cordis.yml 负责装配；模块无法解析与 apply 抛错的失败通道不同。

## 核心推导

把插件抽象为 P:Context→Effect*。配置是一棵插件声明树，loader 将声明解析为运行实例。Context 是能力命名空间，而不是全局可变对象的同义词。

## 工业联系与事实标签

- [THEOREM] 若 apply 是纯函数且输入 Context 相同，其返回描述相同；真实插件的外部副作用使此前提常不成立。
- [EMPIRICAL] 固定提交教程说明配置 entries 并发启动，列表位置不提供依赖顺序。
- [INFERENCE] 组合根与插件实现分离能为同一能力构造 CLI、服务和测试部署。
- [OPEN] 模块解析失败在启动早期的可观测性仍需日志导出配置保证。

## 真实固定 checkout 实战

第 169–175 晚连续复用固定 Harness clone 中的 `tmp/cordis-tutorial`，不得另建一个只依赖自写 mock 的“仿 Harness”目录。课前应已安装依赖；本晚先用 `git rev-parse HEAD` 得到完整的 `47f943859bef60e4160492346772ded9b24f765a`，再按官方第一章原样创建 `hello.ts` 与 `cordis.yml`，从该目录运行：

```sh
node --import tsx ../../vendor/cordis/bin.js
```

保存命令、退出码 0 和 `hello from my first plugin`。随后让 `apply` 抛出教程给出的错误并再次运行，保存非零失败与 `apply exploded`；恢复成功版本，留给后六晚继续修改。

## 严格 60 分钟

- 0–5：闭卷写出 plugin、Context、composition root 三者关系。
- 5–25：精读固定提交第一章 L1–L95。
- 25–37：运行本地 `practice.ts`，完成函数/对象插件、失败和空配置断言。
- 37–42：在真实 clone 核对完整 HEAD，并进入同一个 `tmp/cordis-tutorial`。
- 42–50：按章创建 `hello.ts`、`cordis.yml`，运行仓库 launcher 并记录成功输出。
- 50–55：注入 `apply exploded`，记录真实失败后恢复成功版本。
- 55–60：核对双门证据并写三句复盘。

## 验收

- 本地门：`practice.ts` 的函数/对象插件、`apply` 抛错和空列表断言全部通过。
- 真实门：证据含完整固定 HEAD、launcher 命令与退出码、成功输出、`apply exploded` 失败输出；真实 `hello.ts` 与 `cordis.yml` 已恢复并保留在连续教程工作区。
- 只有两个门都满足才完成本晚；能复述 fixed path 与 commit 不能替代运行证据。

## 可选延伸

精读同目录中文译文 01-first-plugin.zh.md，不计时。
