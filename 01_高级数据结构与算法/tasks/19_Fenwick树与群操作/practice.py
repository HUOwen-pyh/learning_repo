"""第 19 晚：Fenwick 点加、区间和与前缀 lower_bound。"""

from __future__ import annotations

import sys

sys.stdout.reconfigure(encoding="utf-8")

import bisect
import itertools
import random


class Fenwick:
    def __init__(self, n: int) -> None:
        self.tree = [0] * (n + 1)

    def add(self, index: int, delta: int) -> None:
        if not 0 <= index < len(self.tree) - 1:
            raise IndexError(index)
        i = index + 1
        while i < len(self.tree):
            self.tree[i] += delta
            i += i & -i

    def prefix_sum(self, end: int) -> int:
        """a[:end] 的和。"""
        if not 0 <= end < len(self.tree):
            raise IndexError(end)
        total, i = 0, end
        while i:
            total += self.tree[i]
            i -= i & -i
        return total

    def range_sum(self, left: int, right: int) -> int:
        return self.prefix_sum(right) - self.prefix_sum(left)

    def lower_bound(self, target: int) -> int:
        """非负频率下，最小 end 使 prefix_sum(end)>=target；超出返回 n+1。"""
        if target <= 0:
            return 0
        idx, accumulated = 0, 0
        bit = 1 << ((len(self.tree) - 1).bit_length() - 1)
        while bit:
            nxt = idx + bit
            if nxt < len(self.tree) and accumulated + self.tree[nxt] < target:
                idx, accumulated = nxt, accumulated + self.tree[nxt]
            bit >>= 1
        return idx + 1


def main() -> None:
    rng, a, fw = random.Random(19), [0] * 200, Fenwick(200)
    for _ in range(2_000):
        i, delta = rng.randrange(len(a)), rng.randrange(0, 8)
        a[i] += delta
        fw.add(i, delta)
        l, r = sorted((rng.randrange(len(a) + 1), rng.randrange(len(a) + 1)))
        assert fw.range_sum(l, r) == sum(a[l:r])
    prefixes = [0] + list(itertools.accumulate(a))
    for target in range(0, prefixes[-1] + 2, 17):
        assert fw.lower_bound(target) == bisect.bisect_left(prefixes, target)
    print(f"通过：n={len(a)}, total={sum(a)}，随机区间和与 lower_bound 一致。")


if __name__ == "__main__":
    main()

# 动手改造：从初始数组 O(n) 构建 tree，并逐项检查覆盖块不变量。
