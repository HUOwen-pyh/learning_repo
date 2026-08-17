# 第158晚：MCP 工具契约与 JSON-RPC

## 目标与前置

- 目标：实现 tools/list、tools/call、输入 schema 与 JSON-RPC 错误边界。
- 前置：第157晚、JSON Schema、异常处理。

## 计入 60 分钟的必读

| 分钟 | 材料 | 版本 | 精确范围 | 问题 |
|---:|---|---|---|---|
| 12 | [MCP Tools](https://modelcontextprotocol.io/specification/2025-11-25/server/tools) | 2025-11-25 | Listing Tools、Calling Tools、Tool Result | 协议错误与工具执行错误怎样区分？ |
| 8 | [JSON-RPC 2.0](https://www.jsonrpc.org/specification) | 2.0 | Request object、Response object、Error object | id 在通知中为何缺失？ |

## 阅读导引

列出 name、description、inputSchema、outputSchema 的信任边界。先验证 envelope，再验证参数，最后执行；每层失败应返回不同、稳定的错误。

## 核心推导

分派函数 dispatch(req) 是部分函数：非法 envelope 返回 JSON-RPC error；未知方法返回 method not found；合法 tools/call 进入工具层，工具失败可成为带 isError 的结果。不能用 Python traceback 替代协议结构。

## 工业联系与事实标签

- [THEOREM] 若每个成功响应复用请求 id，则并发客户端可按 id 关联响应（id 唯一性仍由客户端保证）。
- [EMPIRICAL] MCP 2025-11-25 工具规范定义了上述消息形状；具体 SDK 可能增加便利封装。
- [INFERENCE] 工具 registry 应冻结名称与 schema 版本，避免运行时静默漂移。
- [OPEN] schema 合法不等于调用被授权，策略与身份必须另行验证。

## 严格 60 分钟

- 0–5：写 envelope；5–25：必读；25–48：运行 registry；48–55：加入参数类型错误；55–60：比较三类失败。

## 验收

list/call、未知方法、缺参数、id=0 边界都有断言。

## 可选延伸

加入 notifications/tools/list_changed，不计时。
