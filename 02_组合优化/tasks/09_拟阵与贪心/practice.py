"""第 09 晚：通用拟阵贪心、两个 oracle 与非拟阵反例。"""
from __future__ import annotations
import sys
sys.stdout.reconfigure(encoding="utf-8", errors="backslashreplace")

from itertools import combinations
from typing import Callable

Oracle = Callable[[set[str]], bool]


def greedy(elements: list[str], weights: dict[str, int], independent: Oracle) -> set[str]:
    chosen: set[str] = set()
    for e in sorted(elements, key=lambda x: (-weights[x], x)):
        if weights[e] > 0 and independent(chosen | {e}):
            chosen.add(e)
    return chosen


def brute(elements: list[str], weights: dict[str, int], independent: Oracle) -> set[str]:
    best: set[str] = set()
    for r in range(len(elements) + 1):
        for combo in combinations(elements, r):
            candidate = set(combo)
            if independent(candidate) and sum(weights[x] for x in candidate) > sum(weights[x] for x in best):
                best = candidate
    return best


def partition_oracle(group: dict[str, str], capacity: dict[str, int]) -> Oracle:
    def independent(chosen: set[str]) -> bool:
        return all(sum(group[x] == g for x in chosen) <= cap for g, cap in capacity.items())
    return independent


def graphic_oracle(endpoints: dict[str, tuple[int, int]]) -> Oracle:
    def independent(chosen: set[str]) -> bool:
        parent = list(range(5))

        def find(x: int) -> int:
            while parent[x] != x:
                parent[x] = parent[parent[x]]
                x = parent[x]
            return x

        for edge in chosen:
            u, v = endpoints[edge]
            a, b = find(u), find(v)
            if a == b:
                return False
            parent[a] = b
        return True
    return independent


def main() -> None:
    items = ["a", "b", "c", "d", "e"]
    group = {"a": "red", "b": "red", "c": "blue", "d": "blue", "e": "blue"}
    pweights = {"a": 8, "b": 7, "c": 6, "d": 5, "e": 4}
    poracle = partition_oracle(group, {"red": 1, "blue": 2})
    pg, pb = greedy(items, pweights, poracle), brute(items, pweights, poracle)
    assert sum(pweights[x] for x in pg) == sum(pweights[x] for x in pb) == 19

    endpoints = {
        "e01": (0, 1), "e12": (1, 2), "e02": (0, 2),
        "e23": (2, 3), "e34": (3, 4), "e24": (2, 4),
    }
    gweights = {"e01": 7, "e12": 6, "e02": 10, "e23": 4, "e34": 3, "e24": 5}
    goracle = graphic_oracle(endpoints)
    gg, gb = greedy(list(endpoints), gweights, goracle), brute(list(endpoints), gweights, goracle)
    assert sum(gweights[x] for x in gg) == sum(gweights[x] for x in gb)

    # 背包是遗传系统但不是拟阵；密度贪心失败。
    knapsack = {"A": (6, 12), "B": (5, 9), "C": (5, 9)}
    density_order = sorted(knapsack, key=lambda x: knapsack[x][1] / knapsack[x][0], reverse=True)
    used = greedy_value = 0
    for x in density_order:
        size, value = knapsack[x]
        if used + size <= 10:
            used += size
            greedy_value += value
    assert greedy_value == 12 < 18
    print("partition greedy =", sorted(pg), "value =", sum(pweights[x] for x in pg))
    print("graphic greedy =", sorted(gg), "value =", sum(gweights[x] for x in gg))
    print("non-matroid density greedy =", greedy_value, "< optimum 18")


if __name__ == "__main__":
    main()

# 动手改造：
# 1. 穷举 A,B 验证交换公理，自动打印第一个失败证据。
# 2. 允许负权，比较“最大权基”和“最大权独立集”的不同。
