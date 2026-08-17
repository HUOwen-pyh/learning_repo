"""第 19 晚：资源约束 DAG 最短路的拉格朗日次梯度法。"""
from __future__ import annotations
import sys
sys.stdout.reconfigure(encoding="utf-8", errors="backslashreplace")

from dataclasses import dataclass
import math


@dataclass(frozen=True)
class Edge:
    u: str
    v: str
    cost: int
    resource: int


EDGES = [
    Edge("s", "a", 2, 4), Edge("a", "t", 2, 4),  # cost 4, resource 8
    Edge("s", "b", 4, 1), Edge("b", "t", 4, 2),  # cost 8, resource 3
    Edge("s", "c", 3, 3), Edge("c", "t", 3, 3),  # cost 6, resource 6
]
ORDER = ["s", "a", "b", "c", "t"]
LIMIT = 4


def lagrangian_shortest(lam: float) -> tuple[list[str], int, int, float]:
    out = {u: [] for u in ORDER}
    for e in EDGES:
        out[e.u].append(e)
    dist = {u: math.inf for u in ORDER}
    pred: dict[str, Edge] = {}
    dist["s"] = 0.0
    for u in ORDER:
        for e in out[u]:
            nd = dist[u] + e.cost + lam * e.resource
            if nd < dist[e.v] - 1e-12:
                dist[e.v], pred[e.v] = nd, e
    path, cost, resource = ["t"], 0, 0
    cur = "t"
    while cur != "s":
        e = pred[cur]
        cost += e.cost
        resource += e.resource
        cur = e.u
        path.append(cur)
    path.reverse()
    lower = cost + lam * (resource - LIMIT)
    return path, cost, resource, lower


def all_paths() -> list[tuple[list[str], int, int]]:
    out = {u: [] for u in ORDER}
    for e in EDGES:
        out[e.u].append(e)
    result = []

    def dfs(u: str, path: list[str], cost: int, resource: int) -> None:
        if u == "t":
            result.append((path[:], cost, resource))
            return
        for e in out[u]:
            dfs(e.v, path + [e.v], cost + e.cost, resource + e.resource)

    dfs("s", ["s"], 0, 0)
    return result


def main() -> None:
    feasible = [p for p in all_paths() if p[2] <= LIMIT]
    optimum_path, optimum, _ = min(feasible, key=lambda p: p[1])
    lam = 0.0
    best_lb = -math.inf
    best_ub = math.inf
    records = []
    for k in range(1, 41):
        path, cost, resource, lower = lagrangian_shortest(lam)
        assert lower <= optimum + 1e-9
        best_lb = max(best_lb, lower)
        if resource <= LIMIT:
            best_ub = min(best_ub, cost)
        violation = resource - LIMIT
        step = 0.25 / math.sqrt(k)
        records.append((k, round(lam, 4), path, resource, round(lower, 4)))
        lam = max(0.0, lam + step * violation)
    assert best_lb <= optimum <= best_ub
    assert best_ub == optimum == 8 and best_lb > 7.0
    print("exact feasible optimum =", optimum, optimum_path)
    print("sample iterations =", records[:3] + records[-3:])
    print("best lower bound =", round(best_lb, 5), "best feasible upper bound =", best_ub)


if __name__ == "__main__":
    main()

# 动手改造：
# 1. 用 Polyak step = theta*(UB-LB)/g^2，并比较收敛轨迹。
# 2. 加入更多边，使拉格朗日最短路含多条同值路径，设计稳定 tie-break。
