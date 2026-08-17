"""第 12 晚：支持插入、查询、删除的跳表。"""

from __future__ import annotations

import sys

sys.stdout.reconfigure(encoding="utf-8")

from dataclasses import dataclass, field
import random


@dataclass
class Node:
    key: int | None
    forward: list["Node | None"] = field(default_factory=list)


class SkipList:
    def __init__(self, rng: random.Random, p: float = 0.5, max_level: int = 16) -> None:
        self.rng, self.p, self.max_level = rng, p, max_level
        self.level = 1
        self.head = Node(None, [None] * max_level)

    def _height(self) -> int:
        h = 1
        while h < self.max_level and self.rng.random() < self.p:
            h += 1
        return h

    def _predecessors(self, key: int) -> list[Node]:
        update = [self.head] * self.max_level
        x = self.head
        for level in range(self.level - 1, -1, -1):
            while x.forward[level] is not None and x.forward[level].key < key:  # type: ignore[operator]
                x = x.forward[level]  # type: ignore[assignment]
            update[level] = x
        return update

    def contains(self, key: int) -> bool:
        x = self._predecessors(key)[0].forward[0]
        return x is not None and x.key == key

    def add(self, key: int) -> bool:
        update = self._predecessors(key)
        if update[0].forward[0] is not None and update[0].forward[0].key == key:
            return False
        h = self._height()
        if h > self.level:
            self.level = h
        node = Node(key, [None] * h)
        for i in range(h):
            node.forward[i] = update[i].forward[i]
            update[i].forward[i] = node
        return True

    def discard(self, key: int) -> bool:
        update = self._predecessors(key)
        target = update[0].forward[0]
        if target is None or target.key != key:
            return False
        for i in range(len(target.forward)):
            if update[i].forward[i] is target:
                update[i].forward[i] = target.forward[i]
        while self.level > 1 and self.head.forward[self.level - 1] is None:
            self.level -= 1
        return True

    def values(self) -> list[int]:
        out, x = [], self.head.forward[0]
        while x is not None:
            assert x.key is not None
            out.append(x.key)
            x = x.forward[0]
        return out


def main() -> None:
    ops, sl, reference = random.Random(120), SkipList(random.Random(12)), set()
    for _ in range(2_000):
        key = ops.randrange(500)
        if ops.random() < 0.55:
            assert sl.add(key) == (key not in reference)
            reference.add(key)
        else:
            assert sl.discard(key) == (key in reference)
            reference.discard(key)
        assert sl.contains(key) == (key in reference)
    assert sl.values() == sorted(reference)
    heights: dict[int, int] = {}
    x = sl.head.forward[0]
    while x:
        heights[len(x.forward)] = heights.get(len(x.forward), 0) + 1
        x = x.forward[0]
    print(f"通过：{len(reference)} 个键，当前层数={sl.level}，高度分布={heights}")


if __name__ == "__main__":
    main()

# 动手改造：实现闭区间 range(lo, hi)，不要从头扫描。
