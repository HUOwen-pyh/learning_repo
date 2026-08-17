"""第 23 晚：二进制倍增 LCA，与朴素参考差分。"""

from __future__ import annotations

import sys

sys.stdout.reconfigure(encoding="utf-8")

from collections import deque
import random


class LCA:
    def __init__(self, graph: list[list[int]], root: int = 0) -> None:
        n = len(graph)
        if n == 0 or not 0 <= root < n or sum(map(len, graph)) != 2 * (n - 1):
            raise ValueError("graph must be a non-empty undirected tree")
        self.depth = [-1] * n
        parent = [root] * n
        self.depth[root] = 0
        queue = deque([root])
        while queue:
            u = queue.popleft()
            for v in graph[u]:
                if self.depth[v] == -1:
                    self.depth[v], parent[v] = self.depth[u] + 1, u
                    queue.append(v)
        if any(d < 0 for d in self.depth):
            raise ValueError("graph must be connected")
        self.up = [parent]
        for _ in range(1, max(1, n.bit_length())):
            prev = self.up[-1]
            self.up.append([prev[prev[v]] for v in range(n)])

    def kth_ancestor(self, v: int, k: int) -> int:
        for bit in range(len(self.up)):
            if k >> bit & 1:
                v = self.up[bit][v]
        return v

    def lca(self, u: int, v: int) -> int:
        if self.depth[u] < self.depth[v]:
            u, v = v, u
        u = self.kth_ancestor(u, self.depth[u] - self.depth[v])
        if u == v:
            return u
        for k in range(len(self.up) - 1, -1, -1):
            if self.up[k][u] != self.up[k][v]:
                u, v = self.up[k][u], self.up[k][v]
        return self.up[0][u]

    def distance(self, u: int, v: int) -> int:
        a = self.lca(u, v)
        return self.depth[u] + self.depth[v] - 2 * self.depth[a]


def naive_lca(parent: list[int], depth: list[int], u: int, v: int) -> int:
    while depth[u] > depth[v]:
        u = parent[u]
    while depth[v] > depth[u]:
        v = parent[v]
    while u != v:
        u, v = parent[u], parent[v]
    return u


def main() -> None:
    n, rng = 600, random.Random(23)
    graph = [[] for _ in range(n)]
    parent = [0] * n
    for v in range(1, n):
        parent[v] = rng.randrange(v)
        graph[v].append(parent[v])
        graph[parent[v]].append(v)
    solver = LCA(graph)
    for _ in range(5_000):
        u, v = rng.randrange(n), rng.randrange(n)
        expected = naive_lca(parent, solver.depth, u, v)
        assert solver.lca(u, v) == expected
        assert solver.distance(u, v) >= abs(solver.depth[u] - solver.depth[v])
    print("通过：随机树上的 5,000 次 LCA 与朴素算法一致。")


if __name__ == "__main__":
    main()

# 动手改造：返回 u 到 v 路径上的第 k 个节点，分 LCA 两侧处理。
