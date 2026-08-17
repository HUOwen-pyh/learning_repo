"""第 07 晚：势函数 + Dijkstra 的逐次最短路最小费用流。"""
from __future__ import annotations
import sys
sys.stdout.reconfigure(encoding="utf-8", errors="backslashreplace")

from dataclasses import dataclass
import heapq
import math


@dataclass
class Edge:
    to: int
    rev: int
    cap: int
    cost: int
    original_cap: int


class MinCostFlow:
    def __init__(self, n: int) -> None:
        self.n = n
        self.g: list[list[Edge]] = [[] for _ in range(n)]
        self.original: list[tuple[int, int]] = []

    def add_edge(self, u: int, v: int, cap: int, cost: int) -> None:
        if cap < 0 or cost < 0:
            raise ValueError("本教学版要求原始容量、费用非负")
        ui, vi = len(self.g[u]), len(self.g[v])
        self.g[u].append(Edge(v, vi, cap, cost, cap))
        self.g[v].append(Edge(u, ui, 0, -cost, 0))
        self.original.append((u, ui))

    def solve(self, source: int, sink: int, demand: int) -> tuple[int, int, list[tuple[list[int], int, int]]]:
        potential = [0] * self.n
        sent = total_cost = 0
        log: list[tuple[list[int], int, int]] = []
        while sent < demand:
            dist = [math.inf] * self.n
            prev: list[tuple[int, int] | None] = [None] * self.n
            dist[source] = 0
            heap: list[tuple[int, int]] = [(0, source)]
            while heap:
                du, u = heapq.heappop(heap)
                if du != dist[u]:
                    continue
                for i, e in enumerate(self.g[u]):
                    if e.cap <= 0:
                        continue
                    reduced = e.cost + potential[u] - potential[e.to]
                    assert reduced >= 0
                    nd = du + reduced
                    if nd < dist[e.to]:
                        dist[e.to], prev[e.to] = nd, (u, i)
                        heapq.heappush(heap, (nd, e.to))
            if prev[sink] is None:
                raise ValueError(f"最多发送 {sent}，需求 {demand} 不可行")
            for v in range(self.n):
                if dist[v] < math.inf:
                    potential[v] += int(dist[v])
            add = demand - sent
            v, path = sink, [sink]
            while v != source:
                u, i = prev[v]  # type: ignore[misc]
                add = min(add, self.g[u][i].cap)
                v = u
                path.append(v)
            path.reverse()
            path_cost = 0
            v = sink
            while v != source:
                u, i = prev[v]  # type: ignore[misc]
                e = self.g[u][i]
                path_cost += e.cost
                e.cap -= add
                self.g[v][e.rev].cap += add
                v = u
            sent += add
            total_cost += add * path_cost
            log.append((path, add, path_cost))
        return sent, total_cost, log

    def flows(self) -> list[tuple[int, int, int, int, int]]:
        return [
            (u, self.g[u][i].to, self.g[u][i].original_cap - self.g[u][i].cap,
             self.g[u][i].original_cap, self.g[u][i].cost)
            for u, i in self.original
        ]


def main() -> None:
    mcf = MinCostFlow(4)  # s=0, a=1, b=2, t=3
    for edge in [(0, 1, 3, 1), (0, 2, 2, 2), (1, 2, 1, 0), (1, 3, 2, 3), (2, 3, 3, 1)]:
        mcf.add_edge(*edge)
    sent, cost, log = mcf.solve(0, 3, 4)
    flows = mcf.flows()
    assert sent == 4 and cost == 12
    assert cost == sum(f * c for _, _, f, _, c in flows)
    balance = [0] * 4
    for u, v, f, cap, _ in flows:
        assert 0 <= f <= cap
        balance[u] -= f
        balance[v] += f
    assert balance == [-4, 0, 0, 4]
    print("augmentations =", log)
    print("flows =", flows)
    print("sent =", sent, "minimum cost =", cost)


if __name__ == "__main__":
    main()

# 动手改造：
# 1. 允许负的原始费用：先用 Bellman-Ford 初始化势。
# 2. 将 demand 改为 6，捕获不可行并输出最多可发送量。
