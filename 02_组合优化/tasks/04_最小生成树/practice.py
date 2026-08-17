"""第 04 晚：Kruskal、Prim 与生成树独立检查。"""
from __future__ import annotations
import sys
sys.stdout.reconfigure(encoding="utf-8", errors="backslashreplace")

import heapq

Edge = tuple[int, int, int]


class DSU:
    def __init__(self, n: int) -> None:
        self.parent = list(range(n))
        self.rank = [0] * n

    def find(self, x: int) -> int:
        while x != self.parent[x]:
            self.parent[x] = self.parent[self.parent[x]]
            x = self.parent[x]
        return x

    def union(self, a: int, b: int) -> bool:
        a, b = self.find(a), self.find(b)
        if a == b:
            return False
        if self.rank[a] < self.rank[b]:
            a, b = b, a
        self.parent[b] = a
        if self.rank[a] == self.rank[b]:
            self.rank[a] += 1
        return True


def kruskal(n: int, edges: list[Edge]) -> list[Edge]:
    dsu, chosen = DSU(n), []
    for u, v, w in sorted(edges, key=lambda e: (e[2], e[0], e[1])):
        if dsu.union(u, v):
            chosen.append((u, v, w))
    return chosen


def prim(n: int, edges: list[Edge], start: int = 0) -> list[Edge]:
    g: list[list[tuple[int, int]]] = [[] for _ in range(n)]
    for u, v, w in edges:
        g[u].append((v, w))
        g[v].append((u, w))
    seen = {start}
    heap = [(w, start, v) for v, w in g[start]]
    heapq.heapify(heap)
    chosen: list[Edge] = []
    while heap:
        w, u, v = heapq.heappop(heap)
        if v in seen:
            continue
        seen.add(v)
        chosen.append((u, v, w))
        for x, wx in g[v]:
            if x not in seen:
                heapq.heappush(heap, (wx, v, x))
    return chosen


def check_tree(n: int, chosen: list[Edge]) -> tuple[bool, int]:
    if len(chosen) != n - 1:
        return False, sum(w for _, _, w in chosen)
    dsu = DSU(n)
    for u, v, _ in chosen:
        if not dsu.union(u, v):
            return False, sum(w for _, _, w in chosen)
    connected = len({dsu.find(i) for i in range(n)}) == 1
    return connected, sum(w for _, _, w in chosen)


def main() -> None:
    edges = [
        (0, 1, 4), (0, 2, 3), (1, 2, 1), (1, 3, 2),
        (2, 3, 4), (3, 4, -1), (2, 4, 6), (4, 5, 2), (3, 5, 5),
    ]
    kt, pt = kruskal(6, edges), prim(6, edges)
    ok_k, kw = check_tree(6, kt)
    ok_p, pw = check_tree(6, pt)
    assert ok_k and ok_p and kw == pw == 7
    cyclic = kt + [(0, 1, 4)]
    assert not check_tree(6, cyclic)[0]
    disconnected_edges = [e for e in edges if 5 not in e[:2]]
    forest = kruskal(6, disconnected_edges)
    assert len(forest) < 5 and not check_tree(6, forest)[0]
    print("Kruskal MST：", kt, "总权", kw)
    print("Prim MST：", pt, "总权", pw)
    print("断边后的最小生成森林边数：", len(forest))


if __name__ == "__main__":
    main()

# 动手改造：
# 1. 对 n<=7 枚举所有 n-1 边子集，作为 MST 真值机。
# 2. 检测给定实例的 MST 是否唯一，并构造不唯一实例。
