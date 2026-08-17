"""第 20 晚：支持半开区间加与区间和的惰性线段树。"""

from __future__ import annotations

import sys

sys.stdout.reconfigure(encoding="utf-8")

import random


class LazySegmentTree:
    def __init__(self, values: list[int]) -> None:
        self.n = len(values)
        self.total = [0] * max(1, 4 * self.n)
        self.lazy = [0] * max(1, 4 * self.n)
        if self.n:
            self._build(1, 0, self.n, values)

    def _build(self, p: int, lo: int, hi: int, a: list[int]) -> None:
        if hi - lo == 1:
            self.total[p] = a[lo]
            return
        mid = (lo + hi) // 2
        self._build(2 * p, lo, mid, a)
        self._build(2 * p + 1, mid, hi, a)
        self.total[p] = self.total[2 * p] + self.total[2 * p + 1]

    def _apply(self, p: int, length: int, delta: int) -> None:
        self.total[p] += length * delta
        self.lazy[p] += delta

    def _push(self, p: int, lo: int, hi: int) -> None:
        if self.lazy[p] and hi - lo > 1:
            mid = (lo + hi) // 2
            self._apply(2 * p, mid - lo, self.lazy[p])
            self._apply(2 * p + 1, hi - mid, self.lazy[p])
            self.lazy[p] = 0

    def add(self, left: int, right: int, delta: int) -> None:
        if not 0 <= left <= right <= self.n:
            raise IndexError

        def visit(p: int, lo: int, hi: int) -> None:
            if right <= lo or hi <= left:
                return
            if left <= lo and hi <= right:
                self._apply(p, hi - lo, delta)
                return
            self._push(p, lo, hi)
            mid = (lo + hi) // 2
            visit(2 * p, lo, mid)
            visit(2 * p + 1, mid, hi)
            self.total[p] = self.total[2 * p] + self.total[2 * p + 1]

        if left < right:
            visit(1, 0, self.n)

    def sum(self, left: int, right: int) -> int:
        if not 0 <= left <= right <= self.n:
            raise IndexError

        def visit(p: int, lo: int, hi: int) -> int:
            if right <= lo or hi <= left:
                return 0
            if left <= lo and hi <= right:
                return self.total[p]
            self._push(p, lo, hi)
            mid = (lo + hi) // 2
            return visit(2 * p, lo, mid) + visit(2 * p + 1, mid, hi)

        return visit(1, 0, self.n) if left < right else 0


def main() -> None:
    rng = random.Random(20)
    a = [rng.randrange(-20, 21) for _ in range(180)]
    tree = LazySegmentTree(a)
    for _ in range(4_000):
        left, right = sorted((rng.randrange(len(a) + 1), rng.randrange(len(a) + 1)))
        if rng.random() < 0.58:
            delta = rng.randrange(-10, 11)
            tree.add(left, right, delta)
            for i in range(left, right):
                a[i] += delta
        else:
            assert tree.sum(left, right) == sum(a[left:right])
    assert tree.sum(0, len(a)) == sum(a)
    print(f"通过：4,000 次区间操作，final sum={sum(a)}。")


if __name__ == "__main__":
    main()

# 动手改造：增加区间最小摘要；注意 delta 对 min 的作用不乘区间长度。
