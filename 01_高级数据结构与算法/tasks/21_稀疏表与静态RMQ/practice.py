"""第 21 晚：幂等 RMQ sparse table 与非重叠静态和表。"""

from __future__ import annotations

import sys

sys.stdout.reconfigure(encoding="utf-8")

import random


class SparseMin:
    def __init__(self, a: list[int]) -> None:
        if not a:
            raise ValueError("non-empty input required")
        self.st = [a.copy()]
        k = 1
        while 1 << k <= len(a):
            half = 1 << (k - 1)
            prev = self.st[-1]
            self.st.append([min(prev[i], prev[i + half]) for i in range(len(a) - (1 << k) + 1)])
            k += 1

    def query(self, left: int, right: int) -> int:
        if not 0 <= left < right <= len(self.st[0]):
            raise IndexError
        k = (right - left).bit_length() - 1
        return min(self.st[k][left], self.st[k][right - (1 << k)])


class DisjointSum:
    """按最高不同位选择分界层的 disjoint sparse table。"""

    def __init__(self, a: list[int]) -> None:
        self.a = a.copy()
        levels = max(1, len(a).bit_length())
        self.table = [[0] * len(a) for _ in range(levels)]
        for k in range(levels):
            block = 1 << (k + 1)
            half = block >> 1
            for start in range(0, len(a), block):
                mid, end = min(start + half, len(a)), min(start + block, len(a))
                if mid > start:
                    self.table[k][mid - 1] = a[mid - 1]
                    for i in range(mid - 2, start - 1, -1):
                        self.table[k][i] = a[i] + self.table[k][i + 1]
                if mid < end:
                    self.table[k][mid] = a[mid]
                    for i in range(mid + 1, end):
                        self.table[k][i] = self.table[k][i - 1] + a[i]

    def query(self, left: int, right: int) -> int:
        if not 0 <= left < right <= len(self.a):
            raise IndexError
        if right - left == 1:
            return self.a[left]
        k = (left ^ (right - 1)).bit_length() - 1
        return self.table[k][left] + self.table[k][right - 1]


def main() -> None:
    rng = random.Random(21)
    a = [rng.randrange(-1_000, 1_001) for _ in range(257)]
    rmq, sums = SparseMin(a), DisjointSum(a)
    for _ in range(5_000):
        l, r = sorted(rng.sample(range(len(a) + 1), 2))
        assert rmq.query(l, r) == min(a[l:r])
        assert sums.query(l, r) == sum(a[l:r])
    print("通过：5,000 个静态区间的 min 与 sum 均和朴素切片一致。")


if __name__ == "__main__":
    main()

# 动手改造：用普通 sparse table 做 gcd；解释其重叠安全性。
