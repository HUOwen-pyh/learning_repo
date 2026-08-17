# 第157晚：MCP 架构与生命周期

## 目标与前置

- 目标：掌握 host/client/server 边界、能力协商与 initialize 生命周期。
- 前置：客户端—服务器、JSON-RPC 2.0、状态机。

## 计入 60 分钟的必读

| 分钟 | 材料 | 版本 | 精确范围 | 问题 |
|---:|---|---|---|---|
| 9 | [MCP Architecture](https://modelcontextprotocol.io/specification/2025-11-25/architecture) | 2025-11-25 | Host、Client、Server 三节 | host 为什么不等于 server？ |
| 11 | [MCP Lifecycle](https://modelcontextprotocol.io/specification/2025-11-25/basic/lifecycle) | 2025-11-25 | Initialization、Operation、Shutdown | initialize 前允许哪些消息？ |

## 阅读导引

画出一个 host 对多个 server 的独立 client 连接。把 protocolVersion、capabilities 与 implementation 信息写入握手状态，不要假定连接成功即功能可用。

## 核心推导

生命周期状态为 NEW→INITIALIZING→READY→CLOSED。initialize 请求协商版本与能力；initialized 通知标记正常操作开始。非法顺序应成为协议错误，而非被宽松忽略。

## 工业联系与事实标签

- [THEOREM] 若状态机只允许上述有向无环转移，CLOSED 不可返回 READY。
- [EMPIRICAL] 所链接的是 MCP 规范 2025-11-25；实现必须声明并协商实际支持版本。
- [INFERENCE] 每个 server 独立能力表可降低错误的跨连接权限继承。
- [OPEN] 远程传输的身份、授权与租户隔离仍需部署系统补充。

## 严格 60 分钟

- 0–5：画边界；5–25：必读；25–48：运行生命周期；48–55：增加版本不匹配；55–60：口述握手不变量。

## 验收

正常顺序、越序操作、重复关闭均测试；能解释 capability negotiation。

## 可选延伸

阅读规范 Transports 页面，不计时。
