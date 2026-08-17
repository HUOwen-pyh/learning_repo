"""第 14 晚：Robin Hood 散列表与后移删除。"""

from __future__ import annotations

import sys

sys.stdout.reconfigure(encoding="utf-8")

import random


def home(key: int, capacity: int) -> int:
    return ((key * 0x9E3779B1) ^ (key >> 16)) % capacity


class RobinHoodMap:
    def __init__(self, capacity: int = 1_024) -> None:
        self.a: list[tuple[int, int] | None] = [None] * capacity
        self.size = 0

    def _distance(self, key: int, index: int) -> int:
        return (index - home(key, len(self.a))) % len(self.a)

    def set(self, key: int, value: int) -> None:
        if self.size * 10 >= len(self.a) * 8:
            raise OverflowError("教学版请保持负载率低于 0.8")
        entry, i, dist = (key, value), home(key, len(self.a)), 0
        for _ in range(len(self.a)):
            current = self.a[i]
            if current is None:
                self.a[i] = entry
                self.size += 1
                return
            if current[0] == key:
                self.a[i] = entry
                return
            current_dist = self._distance(current[0], i)
            if current_dist < dist:
                self.a[i], entry = entry, current
                dist = current_dist
            i = (i + 1) % len(self.a)
            dist += 1
        raise OverflowError

    def _find(self, key: int) -> int:
        i, dist = home(key, len(self.a)), 0
        for _ in range(len(self.a)):
            current = self.a[i]
            if current is None or self._distance(current[0], i) < dist:
                raise KeyError(key)
            if current[0] == key:
                return i
            i = (i + 1) % len(self.a)
            dist += 1
        raise KeyError(key)

    def get(self, key: int) -> int:
        entry = self.a[self._find(key)]
        assert entry is not None
        return entry[1]

    def pop(self, key: int) -> int:
        hole = self._find(key)
        entry = self.a[hole]
        assert entry is not None
        i = (hole + 1) % len(self.a)
        while self.a[i] is not None and self._distance(self.a[i][0], i) > 0:
            self.a[hole] = self.a[i]
            hole, i = i, (i + 1) % len(self.a)
        self.a[hole] = None
        self.size -= 1
        return entry[1]

    def check(self) -> None:
        for i, entry in enumerate(self.a):
            if entry is not None:
                assert self.get(entry[0]) == entry[1]


def main() -> None:
    rng, table, reference = random.Random(14), RobinHoodMap(), {}
    # 键域显著大于表容量，确保发生理想槽冲突并真正触发 Robin Hood 交换。
    for _ in range(1_200):
        key = rng.randrange(20_000)
        if rng.random() < 0.65:
            value = rng.randrange(1_000_000)
            table.set(key, value)
            reference[key] = value
        elif key in reference:
            assert table.pop(key) == reference.pop(key)
        else:
            try:
                table.get(key)
                assert False
            except KeyError:
                pass
    table.check()
    assert table.size == len(reference)
    distances = [table._distance(e[0], i) for i, e in enumerate(table.a) if e]
    print(f"通过：size={table.size}，平均距离={sum(distances)/len(distances):.2f}，最大={max(distances)}")


if __name__ == "__main__":
    main()

# 动手改造：实现 resize；重建时必须重新插入，不能原槽复制。
