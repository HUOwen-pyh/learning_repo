"""第 06 晚：Dinic 最大流与最小割证书。"""
from __future__ import annotations
import sys
sys.stdout.reconfigure(encoding="utf-8", errors="backslashreplace")

from collections import deque
from dataclasses import dataclass


@dataclass
class Edge:
    to: int
    rev: int
    cap: int
    original_cap: int


class Dinic:
    def __init__(self, n: int) -> None:
        self.n = n
        self.g: list[list[Edge]] = [[] for _ in range(n)]
        self.original: list[tuple[int, int]] = []  # (起点, 在邻接表中的位置)

    def add_edge(self, u: int, v: int, cap: int) -> None:
        if cap < 0:
            raise ValueError("容量不能为负")
        ui, vi = len(self.g[u]), len(self.g[v])
        self.g[u].append(Edge(v, vi, cap, cap))
        self.g[v].append(Edge(u, ui, 0, 0))
        self.original.append((u, ui))

    def max_flow(self, source: int, sink: int) -> int:
        if source == sink:
            raise ValueError("源点与汇点必须不同")
        total = 0
        while True:
            level = [-1] * self.n
            level[source] = 0
            q = deque([source])
            while q:
                u = q.popleft()
                for e in self.g[u]:
                    if e.cap > 0 and level[e.to] < 0:
                        level[e.to] = level[u] + 1
                        q.append(e.to)
            if level[sink] < 0:
                return total
            it = [0] * self.n

            def send(u: int, pushed: int) -> int:
                if u == sink:
                    return pushed
                while it[u] < len(self.g[u]):
                    e = self.g[u][it[u]]
                    if e.cap > 0 and level[e.to] == level[u] + 1:
                        got = send(e.to, min(pushed, e.cap))
                        if got:
                            e.cap -= got
                            self.g[e.to][e.rev].cap += got
                            return got
                    it[u] += 1
                return 0

            while (pushed := send(source, 10**18)):
                total += pushed

    def flows(self) -> list[tuple[int, int, int, int]]:
        ans = []
        for u, i in self.original:
            e = self.g[u][i]
            ans.append((u, e.to, e.original_cap - e.cap, e.original_cap))
        return ans

    def residual_reachable(self, source: int) -> set[int]:
        seen = {source}
        q = deque([source])
        while q:
            u = q.popleft()
            for e in self.g[u]:
                if e.cap > 0 and e.to not in seen:
                    seen.add(e.to)
                    q.append(e.to)
        return seen


def check_certificate(
    n: int, source: int, sink: int, flow_value: int,
    flows: list[tuple[int, int, int, int]], cut_side: set[int],
) -> int:
    balance = [0] * n
    for u, v, f, cap in flows:
        assert 0 <= f <= cap
        balance[u] -= f
        balance[v] += f
    assert -balance[source] == balance[sink] == flow_value
    assert all(balance[v] == 0 for v in range(n) if v not in (source, sink))
    assert source in cut_side and sink not in cut_side
    cut_capacity = sum(cap for u, v, _, cap in flows if u in cut_side and v not in cut_side)
    assert cut_capacity == flow_value
    return cut_capacity


def main() -> None:
    solver = Dinic(6)
    for edge in [
        (0, 1, 10), (0, 2, 10), (1, 2, 2), (1, 3, 4),
        (1, 4, 8), (2, 4, 9), (4, 3, 6), (3, 5, 10),
        (4, 5, 10), (0, 1, 1),  # 平行边
    ]:
        solver.add_edge(*edge)
    value = solver.max_flow(0, 5)
    side = solver.residual_reachable(0)
    cut = check_certificate(6, 0, 5, value, solver.flows(), side)
    assert value == cut == 20
    print("max flow =", value)
    print("flow/capacity =", solver.flows())
    print("min-cut source side =", sorted(side), "capacity =", cut)


if __name__ == "__main__":
    main()

# 动手改造：
# 1. 记录每个 blocking-flow 阶段送出的流量和层次数。
# 2. 将一个单位容量二分匹配转成网络，并与第 05 晚结果对照。
