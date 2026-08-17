"""第 23 晚：TSP degree 解的 subtour separation 与有效性验证。"""
from __future__ import annotations
import sys
sys.stdout.reconfigure(encoding="utf-8", errors="backslashreplace")

from itertools import combinations, permutations

Edge = tuple[int, int]


def edge(u: int, v: int) -> Edge:
    return (u, v) if u < v else (v, u)


def cut_value(side: set[int], x: dict[Edge, float], n: int) -> float:
    return sum(value for (u, v), value in x.items() if (u in side) != (v in side))


def separate_subtour(x: dict[Edge, float], n: int) -> tuple[set[int], float]:
    best_side, best_value = set(), float("inf")
    # 固定 0 在 S 中，避免同时枚举补集。
    for size in range(1, n):
        for rest in combinations(range(1, n), size - 1):
            side = {0, *rest}
            if len(side) == n:
                continue
            value = cut_value(side, x, n)
            if value < best_value:
                best_side, best_value = side, value
    return best_side, best_value


def degrees(x: dict[Edge, float], n: int) -> list[float]:
    return [sum(value for e, value in x.items() if v in e) for v in range(n)]


def tour_vector(tour: tuple[int, ...]) -> dict[Edge, float]:
    cycle = (*tour, tour[0])
    return {edge(u, v): 1.0 for u, v in zip(cycle, cycle[1:])}


def main() -> None:
    n = 6
    # 两个互不相连三角形：每点度为2，却不是 Hamiltonian tour。
    x = {
        edge(0, 1): 1.0, edge(1, 2): 1.0, edge(2, 0): 1.0,
        edge(3, 4): 1.0, edge(4, 5): 1.0, edge(5, 3): 1.0,
    }
    assert degrees(x, n) == [2.0] * n
    side, violation_value = separate_subtour(x, n)
    crossing = sorted(e for e in x if (e[0] in side) != (e[1] in side))
    assert violation_value < 2
    # 对所有固定起点的 Hamiltonian tours 检查 x(delta(S))>=2。
    checked = 0
    for perm in permutations(range(1, n)):
        tour_x = tour_vector((0, *perm))
        assert cut_value(side, tour_x, n) >= 2
        checked += 1
    print("degree vector =", degrees(x, n))
    print("violated side S =", sorted(side), "cut value =", violation_value)
    print("positive crossing edges =", crossing)
    print("validity checked on tours =", checked)


if __name__ == "__main__":
    main()

# 动手改造：
# 1. 实现 Stoer-Wagner 全局最小割，替换指数子集枚举。
# 2. 生成分数 2-matching，观察最违反割不一定对应连通分量。
