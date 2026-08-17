"""append-only 事件日志驱动的 mock 工具 agent。"""
from dataclasses import dataclass
from typing import Any, Callable


@dataclass(frozen=True)
class Event:
    seq: int
    kind: str
    data: Any


def execute(name: str, arg: int, tools: dict[str, Callable[[int], int]], allowed: set[str]) -> list[Event]:
    events = [Event(0, "requested", {"name": name, "arg": arg})]
    if name not in allowed:
        return events + [Event(1, "rejected", "policy")]
    result = tools[name](arg)
    return events + [Event(1, "result", result), Event(2, "answered", str(result))]


def replay(events: list[Event]) -> dict[str, Any]:
    state: dict[str, Any] = {"answer": None, "rejected": False}
    for expected, event in enumerate(events):
        if event.seq != expected:
            raise ValueError("non-monotonic sequence")
        if event.kind == "answered":
            state["answer"] = event.data
        elif event.kind == "rejected":
            state["rejected"] = True
    return state


def self_test() -> None:
    log = execute("double", 3, {"double": lambda x: x * 2}, {"double"})
    assert replay(log) == {"answer": "6", "rejected": False}       # 正例
    assert replay(execute("delete", 1, {}, set()))["rejected"]      # 反例
    assert replay([]) == {"answer": None, "rejected": False}       # 边界


if __name__ == "__main__":
    self_test()
    print("161 ok: hands-on: add a hash field and reject tampered event data")
