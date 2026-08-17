"""第 16 晚：Held-Karp TSP 子集 DP、回路重建与下界。"""
from __future__ import annotations
import sys
sys.stdout.reconfigure(encoding="utf-8", errors="backslashreplace")

from itertools import permutations
import math


def distance_matrix(points: list[tuple[int, int]]) -> list[list[float]]:
    return [[math.hypot(x1 - x2, y1 - y2) for x2, y2 in points] for x1, y1 in points]


def held_karp(d: list[list[float]]) -> tuple[float, list[int], int]:
    n = len(d)
    dp: dict[tuple[int, int], float] = {}
    parent: dict[tuple[int, int], int] = {}
    for j in range(1, n):
        mask = (1 << 0) | (1 << j)
        dp[mask, j] = d[0][j]
        parent[mask, j] = 0
    for size in range(3, n + 1):
        for subset in range(1 << n):
            if not (subset & 1) or subset.bit_count() != size:
                continue
            for j in range(1, n):
                if not (subset >> j) & 1:
                    continue
                previous = subset ^ (1 << j)
                choices = [
                    (dp[previous, i] + d[i][j], i)
                    for i in range(1, n)
                    if (previous >> i) & 1 and (previous, i) in dp
                ]
                if size == 3 and previous.bit_count() == 2:
                    # 上面的列表包含唯一非起点；保留显式分支便于读状态。
                    pass
                if choices:
                    dp[subset, j], parent[subset, j] = min(choices)
    full = (1 << n) - 1
    optimum, last = min((dp[full, j] + d[j][0], j) for j in range(1, n))
    backward = [last]
    mask = full
    while backward[-1] != 0:
        j = backward[-1]
        prev = parent[mask, j]
        backward.append(prev)
        mask ^= 1 << j
    tour = list(reversed(backward)) + [0]
    return optimum, tour, len(dp)


def brute_tsp(d: list[list[float]]) -> tuple[float, list[int]]:
    best = (math.inf, [])
    for perm in permutations(range(1, len(d))):
        tour = [0, *perm, 0]
        value = sum(d[u][v] for u, v in zip(tour, tour[1:]))
        if value < best[0]:
            best = (value, tour)
    return best


def mst_weight(nodes: list[int], d: list[list[float]]) -> float:
    in_tree = {nodes[0]}
    total = 0.0
    while len(in_tree) < len(nodes):
        w, v = min(
            (d[u][v], v)
            for u in in_tree for v in nodes if v not in in_tree
        )
        total += w
        in_tree.add(v)
    return total


def one_tree_style_lower_bound(d: list[list[float]]) -> float:
    return mst_weight(list(range(1, len(d))), d) + sum(sorted(d[0][1:])[:2])


def main() -> None:
    points = [(0, 0), (2, 1), (5, 0), (6, 3), (4, 5), (1, 4), (3, 2)]
    d = distance_matrix(points)
    optimum, tour, states = held_karp(d)
    brute, brute_tour = brute_tsp(d)
    lower = one_tree_style_lower_bound(d)
    assert tour[0] == tour[-1] == 0
    assert sorted(tour[:-1]) == list(range(len(points)))
    assert math.isclose(sum(d[u][v] for u, v in zip(tour, tour[1:])), optimum)
    assert math.isclose(optimum, brute)
    assert lower <= optimum + 1e-9
    print("DP states =", states)
    print("tour =", tour, "cost =", round(optimum, 4))
    print("brute tour =", brute_tour)
    print("MST/1-tree-style lower bound =", round(lower, 4))


if __name__ == "__main__":
    main()

# 动手改造：
# 1. 只保留相邻两个 subset-size 层以省内存；思考如何仍重建路径。
# 2. 加入非对称距离，修改下界并找出原论证失效位置。
