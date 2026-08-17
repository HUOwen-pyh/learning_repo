"""第 5 晚：通用 d 叉最小堆，带不变量检查和差分测试。"""

from __future__ import annotations

import sys

sys.stdout.reconfigure(encoding="utf-8")

import heapq
import random


class DaryHeap:
    def __init__(self, values: list[int] | None = None, d: int = 2) -> None:
        if d < 2:
            raise ValueError("d must be >= 2")
        self.d = d
        self.a = [] if values is None else values.copy()
        self.comparisons = 0
        for i in range((len(self.a) - 2) // d, -1, -1):
            self._down(i)

    def push(self, value: int) -> None:
        self.a.append(value)
        i = len(self.a) - 1
        while i:
            p = (i - 1) // self.d
            self.comparisons += 1
            if self.a[p] <= self.a[i]:
                break
            self.a[p], self.a[i] = self.a[i], self.a[p]
            i = p

    def pop(self) -> int:
        if not self.a:
            raise IndexError("pop from empty heap")
        root = self.a[0]
        last = self.a.pop()
        if self.a:
            self.a[0] = last
            self._down(0)
        return root

    def _down(self, i: int) -> None:
        n = len(self.a)
        while True:
            first = self.d * i + 1
            if first >= n:
                return
            best = first
            for child in range(first + 1, min(first + self.d, n)):
                self.comparisons += 1
                if self.a[child] < self.a[best]:
                    best = child
            self.comparisons += 1
            if self.a[i] <= self.a[best]:
                return
            self.a[i], self.a[best] = self.a[best], self.a[i]
            i = best

    def check(self) -> None:
        for i in range(1, len(self.a)):
            assert self.a[(i - 1) // self.d] <= self.a[i]


def main() -> None:
    rng = random.Random(5)
    for d in (2, 4, 8):
        initial = [rng.randrange(10_000) for _ in range(300)]
        ours, reference = DaryHeap(initial, d), initial.copy()
        heapq.heapify(reference)
        for _ in range(800):
            if reference and rng.random() < 0.55:
                assert ours.pop() == heapq.heappop(reference)
            else:
                x = rng.randrange(10_000)
                ours.push(x)
                heapq.heappush(reference, x)
            ours.check()
        assert [ours.pop() for _ in range(len(ours.a))] == [heapq.heappop(reference) for _ in range(len(reference))]
        print(f"d={d}: 差分测试通过，键比较={ours.comparisons}")


if __name__ == "__main__":
    main()

# 动手改造：为元素添加递增 sequence，使相同优先级时保持插入顺序。
