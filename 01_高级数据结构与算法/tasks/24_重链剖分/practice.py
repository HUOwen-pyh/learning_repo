"""第 24 晚：HLD + Fenwick 的点更新、节点路径和。"""

from __future__ import annotations

import sys

sys.stdout.reconfigure(encoding="utf-8")

import random


class Fenwick:
    def __init__(self, n: int) -> None:
        self.t = [0] * (n + 1)

    def add(self, i: int, delta: int) -> None:
        i += 1
        while i < len(self.t):
            self.t[i] += delta
            i += i & -i

    def prefix(self, end: int) -> int:
        total = 0
        while end:
            total += self.t[end]
            end -= end & -end
        return total

    def range_sum(self, left: int, right: int) -> int:
        return self.prefix(right) - self.prefix(left)


class HLD:
    def __init__(self, graph: list[list[int]], values: list[int]) -> None:
        n = len(graph)
        self.parent, self.depth, self.size = [-1] * n, [0] * n, [1] * n
        self.heavy = [-1] * n
        order = [0]
        for u in order:
            for v in graph[u]:
                if v != self.parent[u]:
                    self.parent[v], self.depth[v] = u, self.depth[u] + 1
                    order.append(v)
        for u in reversed(order):
            best = 0
            for v in graph[u]:
                if self.parent[v] == u:
                    self.size[u] += self.size[v]
                    if self.size[v] > best:
                        best, self.heavy[u] = self.size[v], v
        self.head, self.pos = [0] * n, [0] * n
        cursor, stack = 0, [(0, 0)]
        while stack:
            start, head = stack.pop()
            u = start
            while u != -1:
                self.head[u], self.pos[u] = head, cursor
                cursor += 1
                for v in reversed(graph[u]):
                    if self.parent[v] == u and v != self.heavy[u]:
                        stack.append((v, v))
                u = self.heavy[u]
        assert cursor == n and len(set(self.pos)) == n
        self.values = values.copy()
        self.bit = Fenwick(n)
        for v, value in enumerate(values):
            self.bit.add(self.pos[v], value)

    def set(self, v: int, value: int) -> None:
        self.bit.add(self.pos[v], value - self.values[v])
        self.values[v] = value

    def path_sum(self, u: int, v: int) -> int:
        total = 0
        while self.head[u] != self.head[v]:
            if self.depth[self.head[u]] < self.depth[self.head[v]]:
                u, v = v, u
            h = self.head[u]
            total += self.bit.range_sum(self.pos[h], self.pos[u] + 1)
            u = self.parent[h]
        if self.depth[u] > self.depth[v]:
            u, v = v, u
        return total + self.bit.range_sum(self.pos[u], self.pos[v] + 1)


def naive_path_sum(parent: list[int], depth: list[int], values: list[int], u: int, v: int) -> int:
    total = 0
    while u != v:
        if depth[u] >= depth[v]:
            total += values[u]
            u = parent[u]
        else:
            total += values[v]
            v = parent[v]
    return total + values[u]


def main() -> None:
    n, rng = 350, random.Random(24)
    graph = [[] for _ in range(n)]
    for v in range(1, n):
        p = rng.randrange(v)
        graph[p].append(v)
        graph[v].append(p)
    values = [rng.randrange(-30, 31) for _ in range(n)]
    hld = HLD(graph, values)
    for _ in range(3_000):
        if rng.random() < 0.3:
            v, value = rng.randrange(n), rng.randrange(-30, 31)
            values[v] = value
            hld.set(v, value)
        else:
            u, v = rng.randrange(n), rng.randrange(n)
            assert hld.path_sum(u, v) == naive_path_sum(hld.parent, hld.depth, values, u, v)
    print("通过：3,000 次随机点更新/路径和与朴素父链一致。")


if __name__ == "__main__":
    main()

# 动手改造：利用 pos[v] 开始、size[v] 长度，实现 subtree_sum(v)。
