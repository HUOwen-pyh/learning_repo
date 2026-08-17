"""第 16 晚：Count-Min Sketch 频率估计。"""

from __future__ import annotations

import sys

sys.stdout.reconfigure(encoding="utf-8")

import hashlib
import math
import random


class CountMinSketch:
    def __init__(self, epsilon: float, delta: float, seed: bytes = b"cms16") -> None:
        self.w = math.ceil(math.e / epsilon)
        self.d = math.ceil(math.log(1 / delta))
        self.seed = seed
        self.table = [[0] * self.w for _ in range(self.d)]
        self.total = 0

    def _index(self, key: str, row: int) -> int:
        person = (self.seed + row.to_bytes(2, "little"))[:16]
        raw = hashlib.blake2b(key.encode(), digest_size=8, person=person).digest()
        return int.from_bytes(raw, "little") % self.w

    def add(self, key: str, count: int = 1) -> None:
        if count < 0:
            raise ValueError("本实现只支持 cash-register（非负更新）模型")
        for row in range(self.d):
            self.table[row][self._index(key, row)] += count
        self.total += count

    def estimate(self, key: str) -> int:
        return min(self.table[row][self._index(key, row)] for row in range(self.d))

    def merge(self, other: "CountMinSketch") -> None:
        if (self.w, self.d, self.seed) != (other.w, other.d, other.seed):
            raise ValueError("incompatible sketches")
        for r in range(self.d):
            for c in range(self.w):
                self.table[r][c] += other.table[r][c]
        self.total += other.total


def main() -> None:
    epsilon, delta, rng = 0.01, 0.01, random.Random(16)
    left, right, exact = CountMinSketch(epsilon, delta), CountMinSketch(epsilon, delta), {}
    for i in range(40_000):
        # 平方变换制造偏斜流量，低编号更常见。
        key = f"k{int((rng.random() ** 2) * 2_000)}"
        (left if i % 2 else right).add(key)
        exact[key] = exact.get(key, 0) + 1
    left.merge(right)
    errors = []
    for key, true_count in exact.items():
        estimate = left.estimate(key)
        assert estimate >= true_count
        errors.append(estimate - true_count)
    assert max(errors) <= epsilon * left.total  # 本固定实验的实测结果
    print(f"w={left.w}, d={left.d}, total={left.total}, mean_error={sum(errors)/len(errors):.2f}, max={max(errors)}")


if __name__ == "__main__":
    main()

# 动手改造：conservative update 只增加当前最小计数格，比较误差分布。
