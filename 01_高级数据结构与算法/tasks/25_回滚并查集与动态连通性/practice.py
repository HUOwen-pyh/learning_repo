"""第 25 晚：时间线段树 + 回滚 DSU 的离线动态连通性。"""

from __future__ import annotations

import sys

sys.stdout.reconfigure(encoding="utf-8")

from collections import deque
import random

Edge = tuple[int, int]
Operation = tuple[str, int, int]


class RollbackDSU:
    def __init__(self, n: int) -> None:
        self.parent = list(range(n))
        self.size = [1] * n
        self.history: list[tuple[int, int, int] | None] = []

    def find(self, x: int) -> int:
        while x != self.parent[x]:
            x = self.parent[x]
        return x

    def union(self, a: int, b: int) -> None:
        a, b = self.find(a), self.find(b)
        if a == b:
            self.history.append(None)
            return
        if self.size[a] < self.size[b]:
            a, b = b, a
        self.history.append((b, self.size[a], self.parent[b]))
        self.parent[b] = a
        self.size[a] += self.size[b]

    def snapshot(self) -> int:
        return len(self.history)

    def rollback(self, snapshot: int) -> None:
        while len(self.history) > snapshot:
            change = self.history.pop()
            if change is not None:
                child, old_parent_size, old_parent = change
                parent = self.parent[child]
                self.size[parent] = old_parent_size
                self.parent[child] = old_parent


def offline_connectivity(n: int, ops: list[Operation]) -> list[bool]:
    t = len(ops)
    tree: list[list[Edge]] = [[] for _ in range(max(1, 4 * t))]
    active: dict[Edge, int] = {}
    intervals: list[tuple[int, int, Edge]] = []
    for time, (kind, u, v) in enumerate(ops):
        edge = (min(u, v), max(u, v))
        if kind == "add":
            if edge in active:
                raise ValueError("duplicate add")
            active[edge] = time
        elif kind == "remove":
            if edge not in active:
                raise ValueError("remove inactive edge")
            intervals.append((active.pop(edge), time, edge))
    intervals.extend((start, t, edge) for edge, start in active.items())

    def place(p: int, lo: int, hi: int, left: int, right: int, edge: Edge) -> None:
        if right <= lo or hi <= left:
            return
        if left <= lo and hi <= right:
            tree[p].append(edge)
            return
        mid = (lo + hi) // 2
        place(2 * p, lo, mid, left, right, edge)
        place(2 * p + 1, mid, hi, left, right, edge)

    for left, right, edge in intervals:
        if left < right:
            place(1, 0, t, left, right, edge)

    dsu, answers = RollbackDSU(n), []

    def solve(p: int, lo: int, hi: int) -> None:
        snap = dsu.snapshot()
        for u, v in tree[p]:
            dsu.union(u, v)
        if hi - lo == 1:
            kind, u, v = ops[lo]
            if kind == "query":
                answers.append(dsu.find(u) == dsu.find(v))
        else:
            mid = (lo + hi) // 2
            solve(2 * p, lo, mid)
            solve(2 * p + 1, mid, hi)
        dsu.rollback(snap)

    if t:
        solve(1, 0, t)
    return answers


def naive_answers(n: int, ops: list[Operation]) -> list[bool]:
    edges: set[Edge] = set()
    out = []
    for kind, u, v in ops:
        edge = (min(u, v), max(u, v))
        if kind == "add":
            edges.add(edge)
        elif kind == "remove":
            edges.remove(edge)
        else:
            graph = [[] for _ in range(n)]
            for a, b in edges:
                graph[a].append(b)
                graph[b].append(a)
            seen, q = {u}, deque([u])
            while q:
                x = q.popleft()
                for y in graph[x]:
                    if y not in seen:
                        seen.add(y)
                        q.append(y)
            out.append(v in seen)
    return out


def main() -> None:
    n, rng, active, ops = 35, random.Random(25), set(), []
    for _ in range(500):
        u, v = rng.sample(range(n), 2)
        edge = (min(u, v), max(u, v))
        roll = rng.random()
        if roll < 0.35 and edge not in active:
            active.add(edge)
            ops.append(("add", u, v))
        elif roll < 0.55 and active:
            edge = rng.choice(tuple(active))
            active.remove(edge)
            ops.append(("remove", *edge))
        else:
            ops.append(("query", u, v))
    got, expected = offline_connectivity(n, ops), naive_answers(n, ops)
    assert got == expected
    print(f"通过：{len(ops)} 个动态操作，{len(got)} 次查询与逐时刻 BFS 一致。")


if __name__ == "__main__":
    main()

# 动手改造：RollbackDSU 维护 components，并支持每个时间点查询分量数。
