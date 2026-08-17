"""可复现的小型分支调度器。"""
from dataclasses import dataclass


@dataclass(frozen=True)
class State:
    text: str
    cost: int


def schedule(targets: tuple[str, ...], budget: int) -> tuple[list[str], list[str]]:
    queue = [State("", 0)]
    done: list[str] = []
    trace: list[str] = []
    while queue:
        state = queue.pop(0)
        trace.append(state.text)
        if state.text in targets:
            done.append(state.text)
            continue
        if state.cost >= budget:
            continue
        viable = sorted({t[len(state.text)] for t in targets if t.startswith(state.text) and len(t) > len(state.text)})
        queue.extend(State(state.text + token, state.cost + 1) for token in viable)
    return sorted(done), trace


def self_test() -> None:
    values, trace = schedule(("ab", "ac"), 2)
    assert values == ["ab", "ac"]                         # 正例
    assert schedule(("abc",), 2)[0] == []                 # 反例：预算不足
    assert schedule(("",), 0)[0] == [""]                 # 边界
    assert trace[:2] == ["", "a"]


if __name__ == "__main__":
    self_test()
    print("149 ok: hands-on: replace pop(0) with a min-cost priority queue")
