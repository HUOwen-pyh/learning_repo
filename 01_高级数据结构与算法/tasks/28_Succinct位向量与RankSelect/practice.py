"""第 28 晚：64-bit packed 位向量的 rank/select 原型。"""

from __future__ import annotations

import sys

sys.stdout.reconfigure(encoding="utf-8")

import bisect
import random

WORD = 64


class BitVector:
    def __init__(self, bits: list[int]) -> None:
        self.n = len(bits)
        self.words = [0] * ((self.n + WORD - 1) // WORD)
        for i, bit in enumerate(bits):
            if bit not in (0, 1):
                raise ValueError("bits must be 0/1")
            self.words[i // WORD] |= bit << (i % WORD)
        self.prefix = [0]
        for word in self.words:
            self.prefix.append(self.prefix[-1] + word.bit_count())

    def rank1(self, end: int) -> int:
        if not 0 <= end <= self.n:
            raise IndexError(end)
        word, offset = divmod(end, WORD)
        total = self.prefix[word]
        if offset and word < len(self.words):
            total += (self.words[word] & ((1 << offset) - 1)).bit_count()
        return total

    def select1(self, k: int) -> int:
        if not 0 <= k < self.prefix[-1]:
            raise IndexError(k)
        word_index = bisect.bisect_right(self.prefix, k) - 1
        remaining = k - self.prefix[word_index]
        word = self.words[word_index]
        for offset in range(WORD):
            if word >> offset & 1:
                if remaining == 0:
                    position = word_index * WORD + offset
                    assert position < self.n
                    return position
                remaining -= 1
        raise AssertionError("unreachable")


def main() -> None:
    rng = random.Random(28)
    for n in (0, 1, 63, 64, 65, 257, 2_000):
        bits = [rng.randrange(2) for _ in range(n)]
        vector = BitVector(bits)
        for end in range(n + 1):
            assert vector.rank1(end) == sum(bits[:end])
        ones = [i for i, bit in enumerate(bits) if bit]
        assert [vector.select1(k) for k in range(len(ones))] == ones
    print("通过：跨 64-bit 边界的 rank/select 与朴素实现一致。")


if __name__ == "__main__":
    main()

# 动手改造：词内 select 用反复清除最低位实现，并比较操作数。
