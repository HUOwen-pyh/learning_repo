"""第 4 晚：带路径压缩和按大小合并的并查集。"""

from __future__ import annotations

import sys

sys.stdout.reconfigure(encoding="utf-8")

import random


class DSU:
    def __init__(self, n: int) -> None:
        self.parent = list(range(n))
        self.size = [1] * n
        self.components = n

    def find(self, x: int) -> int:
        root = x
        while root != self.parent[root]:
            root = self.parent[root]
        while x != root:
            parent = self.parent[x]
            self.parent[x] = root
            x = parent
        return root

    def union(self, a: int, b: int) -> bool:
        ra, rb = self.find(a), self.find(b)
        if ra == rb:
            return False
        if self.size[ra] < self.size[rb]:
            ra, rb = rb, ra
        self.parent[rb] = ra
        self.size[ra] += self.size[rb]
        self.components -= 1
        return True

    def component_size(self, x: int) -> int:
        return self.size[self.find(x)]

    def check(self) -> None:
        roots = {self.find(i) for i in range(len(self.parent))}
        assert len(roots) == self.components
        assert sum(self.size[r] for r in roots) == len(self.parent)


def main() -> None:
    n, rng = 80, random.Random(11)
    dsu = DSU(n)
    labels = list(range(n))  # 慢但显然正确的参考实现
    for _ in range(600):
        a, b = rng.randrange(n), rng.randrange(n)
        expected_merge = labels[a] != labels[b]
        old, new = labels[b], labels[a]
        if expected_merge:
            labels = [new if x == old else x for x in labels]
        assert dsu.union(a, b) == expected_merge
        for _ in range(3):
            x, y = rng.randrange(n), rng.randrange(n)
            assert (dsu.find(x) == dsu.find(y)) == (labels[x] == labels[y])
    dsu.check()
    sizes = sorted((dsu.component_size(r) for r in {dsu.find(i) for i in range(n)}), reverse=True)
    print(f"通过：components={dsu.components}, sizes={sizes}")


if __name__ == "__main__":
    main()

# 动手改造：读入边流，输出第一条让 union 返回 False 的冗余边。
