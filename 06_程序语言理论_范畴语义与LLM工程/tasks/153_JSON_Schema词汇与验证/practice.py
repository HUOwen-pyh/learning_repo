"""刻意受限的 JSON Schema 2020-12 子集验证器。"""
from typing import Any


PY_TYPES = {"object": dict, "array": list, "string": str, "integer": int, "boolean": bool}


def validate(schema: dict[str, Any], value: Any, path: str = "$") -> list[str]:
    errors: list[str] = []
    expected = schema.get("type")
    if expected and (expected not in PY_TYPES or type(value) is not PY_TYPES[expected]):
        return [f"{path}: expected {expected}"]
    if isinstance(value, dict):
        for key in schema.get("required", []):
            if key not in value:
                errors.append(f"{path}.{key}: required")
        for key, sub in schema.get("properties", {}).items():
            if key in value:
                errors.extend(validate(sub, value[key], f"{path}.{key}"))
    if isinstance(value, list) and "items" in schema:
        for i, item in enumerate(value):
            errors.extend(validate(schema["items"], item, f"{path}[{i}]"))
    return errors


def self_test() -> None:
    s = {"type": "object", "required": ["n"], "properties": {"n": {"type": "integer"}}}
    assert validate(s, {"n": 3}) == []                        # 正例
    assert validate(s, {}) == ["$.n: required"]              # 反例
    assert validate({"type": "array", "items": {"type": "string"}}, []) == []  # 边界
    assert validate(s, {"n": True}) == ["$.n: expected integer"]


if __name__ == "__main__":
    self_test()
    print("153 ok: hands-on: implement minimum without confusing bool and int")
