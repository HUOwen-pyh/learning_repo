"""最小 JSON-RPC 2.0 / MCP tools 分派器。"""
from collections.abc import Callable
from typing import Any


class ToolExecutionError(Exception):
    """参数已通过协议校验，但工具的业务执行失败。"""


def add(arguments: dict[str, Any]) -> int:
    result = arguments["x"] + arguments["y"]
    if abs(result) > 100:
        raise ToolExecutionError("sum exceeds the demo tool's business limit")
    return result


TOOLS: dict[str, Callable[[dict[str, Any]], Any]] = {"add": add}
ADD_SCHEMA = {
    "type": "object",
    "properties": {"x": {"type": "integer"}, "y": {"type": "integer"}},
    "required": ["x", "y"],
    "additionalProperties": False,
}


def rpc_error(request_id: Any, code: int, message: str) -> dict[str, Any]:
    return {"jsonrpc": "2.0", "id": request_id, "error": {"code": code, "message": message}}


def valid_id(value: Any) -> bool:
    return value is None or (isinstance(value, (str, int)) and not isinstance(value, bool))


def valid_add_arguments(arguments: Any) -> bool:
    return (
        isinstance(arguments, dict)
        and set(arguments) == {"x", "y"}
        and all(isinstance(arguments[name], int) and not isinstance(arguments[name], bool) for name in ("x", "y"))
    )


def dispatch(req: Any) -> dict[str, Any] | None:
    """分派一个已解析的 JSON 值；合法 notification 不产生响应。"""
    if not isinstance(req, dict):
        return rpc_error(None, -32600, "Invalid Request")

    request_id = req.get("id")
    if req.get("jsonrpc") != "2.0" or not isinstance(req.get("method"), str) or not valid_id(request_id):
        return rpc_error(None, -32600, "Invalid Request")
    notification = "id" not in req

    def respond(result: dict[str, Any]) -> dict[str, Any] | None:
        return None if notification else {"jsonrpc": "2.0", "id": request_id, "result": result}

    def fail(code: int, message: str) -> dict[str, Any] | None:
        return None if notification else rpc_error(request_id, code, message)

    if "params" in req and not isinstance(req["params"], dict):
        return fail(-32602, "Invalid params")

    if req["method"] == "tools/list":
        return respond({"tools": [{
            "name": "add",
            "description": "Add two integers whose sum stays within [-100, 100].",
            "inputSchema": ADD_SCHEMA,
        }]})

    if req["method"] != "tools/call":
        return fail(-32601, "Method not found")

    params = req.get("params", {})
    name = params.get("name")
    arguments = params.get("arguments", {})
    if name not in TOOLS:
        return fail(-32602, "Invalid params: unknown tool")
    if name == "add" and not valid_add_arguments(arguments):
        return fail(-32602, "Invalid params: arguments do not match inputSchema")

    try:
        value = TOOLS[name](arguments)
        return respond({"content": [{"type": "text", "text": str(value)}], "isError": False})
    except ToolExecutionError as exc:
        # MCP 工具执行失败仍是成功的 JSON-RPC result；错误对模型可见。
        return respond({"content": [{"type": "text", "text": str(exc)}], "isError": True})


def self_test() -> None:
    ok = dispatch({"jsonrpc": "2.0", "id": 1, "method": "tools/call", "params": {"name": "add", "arguments": {"x": 2, "y": 3}}})
    assert ok is not None and ok["result"]["content"] == [{"type": "text", "text": "5"}]
    assert dispatch({"jsonrpc": "1.0", "id": 7, "method": "tools/list"})["error"]["code"] == -32600
    bad_params = dispatch({"jsonrpc": "2.0", "id": 2, "method": "tools/call", "params": {"name": "add", "arguments": {"x": 1}}})
    assert bad_params is not None and bad_params["error"]["code"] == -32602
    execution = dispatch({"jsonrpc": "2.0", "id": 3, "method": "tools/call", "params": {"name": "add", "arguments": {"x": 80, "y": 30}}})
    assert execution is not None and execution["result"]["isError"] is True
    assert execution["result"]["content"][0]["type"] == "text"
    assert dispatch({"jsonrpc": "2.0", "id": 4, "method": "bad"})["error"]["code"] == -32601
    assert dispatch({"jsonrpc": "2.0", "id": 0, "method": "tools/list"})["id"] == 0  # 边界
    assert dispatch({"jsonrpc": "2.0", "method": "tools/list"}) is None  # notification


if __name__ == "__main__":
    self_test()
    print("158 ok: hands-on: add a second schema-validated tool and one business error")
