"""Validation 对照，以及最小 ExceptT over State 与 lift。"""
from __future__ import annotations

import sys
from collections.abc import Callable
from typing import TypeAlias

sys.stdout.reconfigure(encoding="utf-8")

Result: TypeAlias = tuple[str, object]
State: TypeAlias = Callable[[int], tuple[object, int]]
ExceptT: TypeAlias = Callable[[int], tuple[Result, int]]


def validate(record: dict[str, object]) -> list[str] | dict[str, object]:
    errors: list[str] = []
    if not isinstance(record.get("name"), str):
        errors.append("name:string")
    age = record.get("age")
    if type(age) is not int:  # bool 是 int 的子类，但不是合法年龄。
        errors.append("age:int")
    elif age < 0:
        errors.append("age>=0")
    return errors or record


def short_validate(record: dict[str, object]) -> str | dict[str, object]:
    if not isinstance(record.get("name"), str):
        return "name:string"
    age = record.get("age")
    if type(age) is not int:
        return "age:int"
    if age < 0:
        return "age>=0"
    return record


def pure_except(value: object) -> ExceptT:
    return lambda state: (("ok", value), state)


def throw(error: str) -> ExceptT:
    return lambda state: (("error", error), state)


def bind(action: ExceptT, then: Callable[[object], ExceptT]) -> ExceptT:
    def run(state: int) -> tuple[Result, int]:
        result, next_state = action(state)
        if result[0] == "error":
            return result, next_state
        return then(result[1])(next_state)

    return run


def lift(action: State) -> ExceptT:
    """把底层 State 动作嵌入 ExceptT，同时保留状态变化。"""
    def run(state: int) -> tuple[Result, int]:
        value, next_state = action(state)
        return ("ok", value), next_state

    return run


def main() -> None:
    bad = {"name": 1, "age": "old"}
    assert validate(bad) == ["name:string", "age:int"]
    assert short_validate(bad) == "name:string"
    assert validate({"name": "Ada", "age": True}) == ["age:int"]
    good = {"name": "Ada", "age": 36}
    assert validate(good) == short_validate(good) == good

    tick: State = lambda state: (state, state + 1)
    lifted = bind(lift(tick), lambda old: pure_except(int(old) * 2))
    assert lifted(4) == (("ok", 8), 5), "lift 必须保留底层状态变化"
    stopped = bind(throw("invalid"), lambda _: lift(tick))
    assert stopped(4) == (("error", "invalid"), 4), "ExceptT 异常必须短路"
    print("Validation、bool 边界与最小 ExceptT/State lift 测试通过")


if __name__ == "__main__":
    main()

# 动手改造：交换 StateT/ExceptT 顺序，并比较“异常后状态是否保留”。
