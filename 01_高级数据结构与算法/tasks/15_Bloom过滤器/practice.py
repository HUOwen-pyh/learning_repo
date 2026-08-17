"""第 15 晚：参数化 Bloom filter 与假阳性实验。"""

from __future__ import annotations

import sys

sys.stdout.reconfigure(encoding="utf-8")

import hashlib
import math
import random


class BloomFilter:
    def __init__(self, capacity: int, false_positive_rate: float) -> None:
        if capacity <= 0 or not 0 < false_positive_rate < 1:
            raise ValueError
        self.m = max(8, math.ceil(-capacity * math.log(false_positive_rate) / math.log(2) ** 2))
        self.k = max(1, round(self.m / capacity * math.log(2)))
        self.bits = bytearray((self.m + 7) // 8)

    def _positions(self, item: str):
        digest = hashlib.blake2b(item.encode(), digest_size=16, person=b"night15").digest()
        h1, h2 = int.from_bytes(digest[:8], "little"), int.from_bytes(digest[8:], "little") | 1
        for i in range(self.k):
            yield (h1 + i * h2) % self.m

    def add(self, item: str) -> None:
        for p in self._positions(item):
            self.bits[p // 8] |= 1 << (p % 8)

    def __contains__(self, item: str) -> bool:
        return all(self.bits[p // 8] & (1 << (p % 8)) for p in self._positions(item))


def main() -> None:
    n, target, rng = 5_000, 0.01, random.Random(15)
    bf = BloomFilter(n, target)
    inserted = {f"in-{rng.getrandbits(80)}" for _ in range(n)}
    for x in inserted:
        bf.add(x)
    assert all(x in bf for x in inserted)  # 无假阴性
    probes = [f"out-{rng.getrandbits(80)}" for _ in range(30_000)]
    false_positives = sum(x in bf for x in probes if x not in inserted)
    measured = false_positives / len(probes)
    # 概率实验只用宽松上限防明显实现错误，不把随机波动当确定定理。
    assert measured < 0.02
    print(f"m={bf.m} bits, k={bf.k}, bits/item={bf.m/n:.2f}, measured FP={measured:.3%}")


if __name__ == "__main__":
    main()

# 动手改造：分别使用 4、8、12 bits/item，输出理论和实测假阳性率。
