"""第 03 晚：Dijkstra、Bellman-Ford、路径与负环证书。"""
from __future__ import annotations
import sys
sys.stdout.reconfigure(encoding="utf-8", errors="backslashreplace")

import heapq
import math

Edge = tuple[str, str, float]


def adjacency(nodes: list[str], edges: list[Edge]) -> dict[str, list[tuple[str, float]]]:
    g = {u: [] for u in nodes}
    for u, v, w in edges:
        g[u].append((v, w))
    return g


def dijkstra(
    nodes: list[str], edges: list[Edge], source: str
) -> tuple[dict[str, float], dict[str, str]]:
    if any(w < 0 for _, _, w in edges):
        raise ValueError("Dijkstra 要求非负边权")
    g = adjacency(nodes, edges)
    dist = {u: math.inf for u in nodes}
    pred: dict[str, str] = {}
    dist[source] = 0.0
    heap = [(0.0, source)]
    while heap:
        du, u = heapq.heappop(heap)
        if du != dist[u]:
            continue
        for v, w in g[u]:
            nd = du + w
            if nd < dist[v]:
                dist[v], pred[v] = nd, u
                heapq.heappush(heap, (nd, v))
    return dist, pred


def bellman_ford(
    nodes: list[str], edges: list[Edge], source: str
) -> tuple[dict[str, float], dict[str, str], list[str] | None]:
    dist = {u: math.inf for u in nodes}
    pred: dict[str, str] = {}
    dist[source] = 0.0
    updated: str | None = None
    for _ in range(len(nodes)):
        updated = None
        for u, v, w in edges:
            if dist[u] != math.inf and dist[v] > dist[u] + w:
                dist[v], pred[v], updated = dist[u] + w, u, v
        if updated is None:
            return dist, pred, None
    assert updated is not None
    y = updated
    for _ in nodes:
        y = pred[y]
    backward = [y]
    cur = pred[y]
    while cur != y:
        backward.append(cur)
        cur = pred[cur]
    backward.append(y)
    return dist, pred, list(reversed(backward))


def path_to(pred: dict[str, str], source: str, target: str) -> list[str]:
    path = [target]
    while path[-1] != source:
        if path[-1] not in pred:
            return []
        path.append(pred[path[-1]])
    return list(reversed(path))


def walk_weight(walk: list[str], edges: list[Edge]) -> float:
    lookup = {(u, v): w for u, v, w in edges}
    return sum(lookup[(u, v)] for u, v in zip(walk, walk[1:]))


def main() -> None:
    nodes = list("ABCDE") + ["Z"]
    edges: list[Edge] = [
        ("A", "B", 4), ("A", "C", 1), ("C", "B", 2),
        ("B", "D", 1), ("C", "D", 5), ("D", "E", 3),
    ]
    dd, dp = dijkstra(nodes, edges, "A")
    bd, bp, cycle = bellman_ford(nodes, edges, "A")
    assert cycle is None and dd == bd
    path = path_to(dp, "A", "E")
    assert path == ["A", "C", "B", "D", "E"]
    assert walk_weight(path, edges) == dd["E"] == 7
    assert math.isinf(dd["Z"])

    negative = [("s", "a", 2), ("s", "b", 5), ("a", "b", -4), ("b", "t", 2)]
    nd, np, nc = bellman_ford(list("sabt"), negative, "s")
    assert nc is None and nd["t"] == 0 and path_to(np, "s", "t") == ["s", "a", "b", "t"]
    try:
        dijkstra(list("sabt"), negative, "s")
        raise AssertionError("负边应被拒绝")
    except ValueError:
        pass

    neg_cycle_edges = [("s", "a", 0), ("a", "b", 1), ("b", "c", -4), ("c", "a", 1)]
    _, _, cert = bellman_ford(list("sabc"), neg_cycle_edges, "s")
    assert cert is not None and cert[0] == cert[-1]
    assert walk_weight(cert, neg_cycle_edges) < 0
    print("最短路径：", path, "距离", dd["E"])
    print("负环证书：", cert, "权重", walk_weight(cert, neg_cycle_edges))


if __name__ == "__main__":
    main()

# 动手改造：
# 1. 用 Bellman-Ford 距离作势，验证所有可达边约化费用非负。
# 2. 加入等长路径，并制定稳定的字典序 tie-break 规则。
