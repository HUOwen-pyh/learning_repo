"""确定性的 ReAct mock loop。"""
from dataclasses import dataclass
from typing import Callable


@dataclass(frozen=True)
class Action:
    name: str
    arg: str


def run(policy: Callable[[list[str]], Action], tools: dict[str, Callable[[str], str]], limit: int) -> list[str]:
    trace: list[str] = []
    for _ in range(limit):
        action = policy(trace)
        trace.append(f"action:{action.name}:{action.arg}")
        if action.name == "finish":
            trace.append(f"answer:{action.arg}")
            return trace
        if action.name not in tools:
            trace.append("error:unknown-tool")
            return trace
        trace.append(f"observation:{tools[action.name](action.arg)}")
    trace.append("error:step-limit")
    return trace


def self_test() -> None:
    policy = lambda t: Action("lookup", "2") if not t else Action("finish", t[-1].split(":")[-1])
    trace = run(policy, {"lookup": lambda x: str(int(x) * 2)}, 2)
    assert trace[-1] == "answer:4"                              # 正例
    assert run(lambda _: Action("bad", ""), {}, 1)[-1] == "error:unknown-tool"
    assert run(lambda _: Action("lookup", "1"), {"lookup": lambda x: x}, 0) == ["error:step-limit"]


if __name__ == "__main__":
    self_test()
    print("155 ok: hands-on: add a policy that must use two different tools")
