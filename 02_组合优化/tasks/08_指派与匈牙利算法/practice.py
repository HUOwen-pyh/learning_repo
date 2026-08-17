"""第 08 晚：O(n^3) 匈牙利算法与 primal-dual 证书。"""
from __future__ import annotations
import sys
sys.stdout.reconfigure(encoding="utf-8", errors="backslashreplace")

from itertools import permutations


def hungarian(cost: list[list[int]]) -> tuple[list[int], int, list[int], list[int]]:
    n = len(cost)
    if n == 0 or any(len(row) != n for row in cost):
        raise ValueError("教学实现要求非空方阵")
    # 1-based；p[j] 是当前匹配到列 j 的行。
    u = [0] * (n + 1)
    v = [0] * (n + 1)
    p = [0] * (n + 1)
    way = [0] * (n + 1)
    for i in range(1, n + 1):
        p[0] = i
        minv = [10**18] * (n + 1)
        used = [False] * (n + 1)
        j0 = 0
        while True:
            used[j0] = True
            i0 = p[j0]
            delta, j1 = 10**18, 0
            for j in range(1, n + 1):
                if used[j]:
                    continue
                cur = cost[i0 - 1][j - 1] - u[i0] - v[j]
                if cur < minv[j]:
                    minv[j], way[j] = cur, j0
                if minv[j] < delta:
                    delta, j1 = minv[j], j
            for j in range(n + 1):
                if used[j]:
                    u[p[j]] += delta
                    v[j] -= delta
                else:
                    minv[j] -= delta
            j0 = j1
            if p[j0] == 0:
                break
        while True:
            j1 = way[j0]
            p[j0] = p[j1]
            j0 = j1
            if j0 == 0:
                break
    assignment = [-1] * n
    for j in range(1, n + 1):
        assignment[p[j] - 1] = j - 1
    value = sum(cost[i][assignment[i]] for i in range(n))
    return assignment, value, u[1:], v[1:]


def brute_force(cost: list[list[int]]) -> tuple[int, tuple[int, ...]]:
    candidates = ((sum(row[j] for row, j in zip(cost, perm)), perm)
                  for perm in permutations(range(len(cost))))
    return min(candidates)


def main() -> None:
    cost = [
        [9, 2, 7, 8],
        [6, 4, 3, 7],
        [5, 8, 1, 8],
        [7, 6, 9, 4],
    ]
    assignment, primal, u, v = hungarian(cost)
    brute, _ = brute_force(cost)
    assert sorted(assignment) == list(range(len(cost)))
    assert primal == brute == 13
    assert all(u[i] + v[j] <= cost[i][j] for i in range(4) for j in range(4))
    assert all(u[i] + v[assignment[i]] == cost[i][assignment[i]] for i in range(4))
    dual = sum(u) + sum(v)
    assert primal == dual
    print("row -> column =", assignment)
    print("primal cost =", primal, "dual value =", dual)
    print("row potentials =", u, "column potentials =", v)


if __name__ == "__main__":
    main()

# 动手改造：
# 1. 用 C-max_profit 把最大收益指派转成最小费用，核对最优排列。
# 2. 给 3x5 矩阵补虚拟行，并解释虚拟成本的业务含义。
