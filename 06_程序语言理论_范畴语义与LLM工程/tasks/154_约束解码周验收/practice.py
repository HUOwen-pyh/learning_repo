"""综合验收：前缀语法、终值结构、业务约束。"""
import json


def prefix_ok(text: str) -> bool:
    return text == "" or "true".startswith(text) or "false".startswith(text)


def decode_bool(tokens: tuple[str, ...], max_steps: int = 5) -> list[bool]:
    frontier, out = [""], []
    for _ in range(max_steps + 1):
        nxt = []
        for prefix in frontier:
            try:
                value = json.loads(prefix)
                if type(value) is bool and value is True:       # 业务谓词：只接受 true
                    out.append(value)
            except json.JSONDecodeError:
                pass
            for token in tokens:
                if prefix_ok(prefix + token):
                    nxt.append(prefix + token)
        frontier = nxt
    return out


def self_test() -> None:
    assert decode_bool(("t", "r", "u", "e")) == [True]       # 正例
    assert decode_bool(("f", "a", "l", "s", "e")) == []    # 业务反例
    assert decode_bool(("x",)) == []                            # 语法反例
    assert decode_bool(()) == []                                # 边界


if __name__ == "__main__":
    self_test()
    print("154 ok: hands-on: accept both booleans, then add a separate policy layer")
