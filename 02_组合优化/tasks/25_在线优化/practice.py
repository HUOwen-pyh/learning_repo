"""第 25 晚：枚举随机 Ranking 与对抗到达序的精确期望。"""
from __future__ import annotations
import sys
sys.stdout.reconfigure(encoding="utf-8", errors="backslashreplace")

from fractions import Fraction as F
from itertools import permutations
import math

OFFLINE = ("a", "b", "c", "d")
ONLINE = ("1", "2", "3", "4")
ADJ = {
    "1": ("a", "b"),
    "2": ("a",),
    "3": ("b", "c"),
    "4": ("c", "d"),
}


def ranking(arrival: tuple[str, ...], rank_order: tuple[str, ...]) -> int:
    rank = {v: i for i, v in enumerate(rank_order)}
    free = set(OFFLINE)
    matched = 0
    for u in arrival:
        candidates = [v for v in ADJ[u] if v in free]
        if candidates:
            v = min(candidates, key=lambda x: rank[x])
            free.remove(v)
            matched += 1
    return matched


def offline_optimum() -> int:
    mate: dict[str, str] = {}

    def augment(u: str, seen: set[str]) -> bool:
        for v in ADJ[u]:
            if v in seen:
                continue
            seen.add(v)
            if v not in mate or augment(mate[v], seen):
                mate[v] = u
                return True
        return False

    return sum(augment(u, set()) for u in ONLINE)


def main() -> None:
    optimum = offline_optimum()
    ranks = list(permutations(OFFLINE))
    results = []
    for arrival in permutations(ONLINE):
        expected = F(sum(ranking(arrival, rank) for rank in ranks), len(ranks))
        results.append((expected / optimum, arrival, expected))
    worst_ratio, worst_arrival, expected = min(results)
    assert optimum == 4
    assert float(worst_ratio) + 1e-12 >= 1 - 1 / math.e
    assert worst_ratio <= 1
    # 每次具体运行也必须是合法匹配大小。
    assert all(0 <= ranking(worst_arrival, r) <= optimum for r in ranks)
    print("offline optimum =", optimum)
    print("worst oblivious arrival =", worst_arrival)
    print("exact expected matching =", expected, "ratio =", worst_ratio)
    print("enumerated arrival/rank pairs =", math.factorial(4) ** 2)


if __name__ == "__main__":
    main()

# 动手改造：
# 1. 穷举小二分图，搜索 Ranking 最差有限规模实例。
# 2. 让 adversary 观察 rank 后选到达序，比较模型改变后的结果。
