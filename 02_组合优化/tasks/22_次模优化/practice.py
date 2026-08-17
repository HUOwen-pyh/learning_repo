"""第 22 晚：带权最大覆盖、穷举真值与次模性全检查。"""
from __future__ import annotations
import sys
sys.stdout.reconfigure(encoding="utf-8", errors="backslashreplace")

from itertools import combinations
import math

SETS = {
    "A": {0, 1, 2, 8},
    "B": {2, 3, 4},
    "C": {4, 5, 6, 9},
    "D": {0, 6, 7},
    "E": {1, 3, 5, 7},
    "F": {8, 9},
}
WEIGHT = {0: 2, 1: 1, 2: 3, 3: 2, 4: 1, 5: 4, 6: 2, 7: 3, 8: 2, 9: 5}


def value(chosen: frozenset[str] | set[str]) -> int:
    covered: set[int] = set()
    for name in chosen:
        covered |= SETS[name]
    return sum(WEIGHT[e] for e in covered)


def greedy(k: int) -> set[str]:
    chosen: set[str] = set()
    for _ in range(k):
        candidate = max(
            (name for name in SETS if name not in chosen),
            key=lambda name: (value(chosen | {name}) - value(chosen), name),
        )
        if value(chosen | {candidate}) == value(chosen):
            break
        chosen.add(candidate)
    return chosen


def brute(k: int) -> set[str]:
    return max(
        (set(c) for r in range(k + 1) for c in combinations(SETS, r)),
        key=value,
    )


def verify_submodular() -> int:
    names = list(SETS)
    subsets = [
        frozenset(c)
        for r in range(len(names) + 1)
        for c in combinations(names, r)
    ]
    checks = 0
    for a in subsets:
        for b in subsets:
            if not a <= b:
                continue
            for e in set(names) - b:
                da = value(a | {e}) - value(a)
                db = value(b | {e}) - value(b)
                assert da >= db >= 0
                checks += 1
    return checks


def main() -> None:
    k = 3
    chosen = greedy(k)
    optimum = brute(k)
    checks = verify_submodular()
    guarantee = (1 - (1 - 1 / k) ** k) * value(optimum)
    assert len(chosen) <= k
    assert value(chosen) >= guarantee - 1e-9
    assert value(chosen) >= (1 - 1 / math.e) * value(optimum)
    print("greedy =", sorted(chosen), "value =", value(chosen))
    print("optimum =", sorted(optimum), "value =", value(optimum))
    print("finite-k guarantee threshold =", round(guarantee, 3))
    print("diminishing-return checks =", checks)


if __name__ == "__main__":
    main()

# 动手改造：
# 1. 为集合加入不同成本，实现按边际/成本 greedy，并寻找失败反例。
# 2. 实现 lazy greedy 的优先队列，统计少算了多少次边际。
