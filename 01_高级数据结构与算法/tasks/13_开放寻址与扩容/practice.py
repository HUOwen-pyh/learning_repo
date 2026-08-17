"""第 13 晚：带墓碑和几何扩容的线性探测映射。"""

from __future__ import annotations

import sys

sys.stdout.reconfigure(encoding="utf-8")

import random

EMPTY, DELETED = object(), object()


def mix(x: int) -> int:
    x = (x ^ (x >> 16)) * 0x45D9F3B
    x = (x ^ (x >> 16)) * 0x45D9F3B
    return x ^ (x >> 16)


class LinearMap:
    def __init__(self, capacity: int = 8) -> None:
        self.table: list[object] = [EMPTY] * capacity
        self.size = 0

    def _slot(self, key: int, for_insert: bool) -> int:
        first_deleted = -1
        start = mix(key) % len(self.table)
        for step in range(len(self.table)):
            i = (start + step) % len(self.table)
            entry = self.table[i]
            if entry is EMPTY:
                return first_deleted if for_insert and first_deleted >= 0 else i
            if entry is DELETED:
                if first_deleted < 0:
                    first_deleted = i
            elif entry[0] == key:  # type: ignore[index]
                return i
        if for_insert and first_deleted >= 0:
            return first_deleted
        raise KeyError(key)

    def __setitem__(self, key: int, value: int) -> None:
        if (self.size + 1) * 10 >= len(self.table) * 7:
            self._resize(2 * len(self.table))
        i = self._slot(key, True)
        if self.table[i] is EMPTY or self.table[i] is DELETED:
            self.size += 1
        self.table[i] = (key, value)

    def __getitem__(self, key: int) -> int:
        i = self._slot(key, False)
        entry = self.table[i]
        if entry is EMPTY or entry is DELETED:
            raise KeyError(key)
        return entry[1]  # type: ignore[index,return-value]

    def pop(self, key: int) -> int:
        i = self._slot(key, False)
        entry = self.table[i]
        if entry is EMPTY or entry is DELETED:
            raise KeyError(key)
        self.table[i] = DELETED
        self.size -= 1
        return entry[1]  # type: ignore[index,return-value]

    def _resize(self, capacity: int) -> None:
        active = [x for x in self.table if x is not EMPTY and x is not DELETED]
        self.table, self.size = [EMPTY] * capacity, 0
        for key, value in active:  # type: ignore[misc]
            self[key] = value


def main() -> None:
    rng, ours, reference = random.Random(13), LinearMap(), {}
    for _ in range(5_000):
        key = rng.randrange(600)
        action = rng.random()
        if action < 0.55:
            value = rng.randrange(1_000_000)
            ours[key] = reference[key] = value
        elif action < 0.75:
            if key in reference:
                assert ours.pop(key) == reference.pop(key)
            else:
                try:
                    ours.pop(key)
                    assert False
                except KeyError:
                    pass
        else:
            if key in reference:
                assert ours[key] == reference[key]
            else:
                try:
                    ours[key]
                    assert False
                except KeyError:
                    pass
        assert ours.size == len(reference)
    assert all(ours[k] == v for k, v in reference.items())
    print(f"通过：size={ours.size}, capacity={len(ours.table)}, load={ours.size/len(ours.table):.2f}")


if __name__ == "__main__":
    main()

# 动手改造：统计成功/失败查询探测数，按负载因子分桶报告。
