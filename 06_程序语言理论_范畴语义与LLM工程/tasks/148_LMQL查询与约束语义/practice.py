"""LMQL 风格的最小查询 IR；只依赖标准库。"""
from enum import Enum, auto
from itertools import product


class Truth(Enum):
    TRUE = auto()
    FALSE = auto()
    UNKNOWN = auto()


class InSet:
    def __init__(self, choices: tuple[str, ...]):
        self.choices = choices

    def partial(self, prefix: str) -> Truth:
        possible = [x for x in self.choices if x.startswith(prefix)]
        if not possible:
            return Truth.FALSE
        return Truth.TRUE if prefix in self.choices else Truth.UNKNOWN


def decode(alphabet: str, max_len: int, constraint: InSet) -> list[str]:
    accepted: list[str] = []
    frontier = [""]
    for _ in range(max_len + 1):
        next_frontier: list[str] = []
        for prefix in frontier:
            state = constraint.partial(prefix)
            if state is Truth.TRUE:
                accepted.append(prefix)
            if state is not Truth.FALSE and len(prefix) < max_len:
                next_frontier.extend(prefix + c for c in alphabet)
        frontier = next_frontier
    return sorted(set(accepted))


def self_test() -> None:
    c = InSet(("YES", "NO"))
    assert decode("YESNO", 3, c) == ["NO", "YES"]       # 正例
    assert c.partial("X") is Truth.FALSE                 # 反例
    assert c.partial("") is Truth.UNKNOWN                # 边界
    assert all(c.partial(p) is not Truth.FALSE for p in ("Y", "YE", "N"))


if __name__ == "__main__":
    self_test()
    print("148 ok: hands-on: edit choices to add MAYBE, then extend max_len and assertions")
