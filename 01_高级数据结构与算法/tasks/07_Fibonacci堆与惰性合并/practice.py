"""第 7 晚：可 meld/decrease-key 的 Fibonacci 最小堆。"""

from __future__ import annotations

import sys

sys.stdout.reconfigure(encoding="utf-8")

from dataclasses import dataclass, field
import random


@dataclass(eq=False)
class Node:
    key: int
    parent: "Node | None" = None
    children: list["Node"] = field(default_factory=list)
    marked: bool = False

    @property
    def degree(self) -> int:
        return len(self.children)


class FibonacciHeap:
    def __init__(self) -> None:
        self.roots: list[Node] = []
        self.minimum: Node | None = None
        self.n = 0

    def push(self, key: int) -> Node:
        node = Node(key)
        self.roots.append(node)
        self.minimum = node if self.minimum is None or key < self.minimum.key else self.minimum
        self.n += 1
        return node

    def meld(self, other: "FibonacciHeap") -> None:
        self.roots.extend(other.roots)
        if other.minimum is not None and (self.minimum is None or other.minimum.key < self.minimum.key):
            self.minimum = other.minimum
        self.n += other.n
        other.roots, other.minimum, other.n = [], None, 0

    def _link(self, child: Node, parent: Node) -> None:
        child.parent = parent
        child.marked = False
        parent.children.append(child)

    def _consolidate(self) -> None:
        by_degree: dict[int, Node] = {}
        for root in self.roots:
            x = root
            while x.degree in by_degree:
                y = by_degree.pop(x.degree)
                if y.key < x.key:
                    x, y = y, x
                self._link(y, x)
            by_degree[x.degree] = x
        self.roots = list(by_degree.values())
        self.minimum = min(self.roots, key=lambda x: x.key, default=None)

    def pop(self) -> int:
        z = self.minimum
        if z is None:
            raise IndexError("pop from empty heap")
        self.roots.remove(z)
        for child in z.children:
            child.parent = None
            child.marked = False
            self.roots.append(child)
        self.n -= 1
        self._consolidate()
        return z.key

    def decrease_key(self, x: Node, new_key: int) -> None:
        if new_key > x.key:
            raise ValueError("key may only decrease")
        x.key = new_key
        parent = x.parent
        if parent is not None and x.key < parent.key:
            self._cut(x, parent)
            self._cascading_cut(parent)
        if self.minimum is None or x.key < self.minimum.key:
            self.minimum = x

    def _cut(self, x: Node, parent: Node) -> None:
        parent.children.remove(x)
        x.parent = None
        x.marked = False
        self.roots.append(x)

    def _cascading_cut(self, x: Node) -> None:
        parent = x.parent
        if parent is None:
            return
        if not x.marked:
            x.marked = True
        else:
            self._cut(x, parent)
            self._cascading_cut(parent)

    def check(self) -> None:
        seen: set[Node] = set()
        stack = self.roots.copy()
        assert all(r.parent is None and not r.marked for r in self.roots)
        while stack:
            node = stack.pop()
            assert node not in seen
            seen.add(node)
            for child in node.children:
                assert child.parent is node and node.key <= child.key
                stack.append(child)
        assert len(seen) == self.n
        assert self.minimum is (min(self.roots, key=lambda x: x.key) if self.roots else None)


def main() -> None:
    rng = random.Random(7)
    heap, live = FibonacciHeap(), []
    for _ in range(120):
        key = rng.randrange(1_000, 10_000)
        live.append(heap.push(key))
    heap.pop()  # 触发第一次 consolidation，产生非根节点
    target = next(node for node in live if node.parent is not None)
    heap.decrease_key(target, -1)
    heap.check()
    result = [heap.pop() for _ in range(heap.n)]
    assert result == sorted(result) and result[0] == -1
    print("通过：decrease-key 切断后，119 个键有序弹出。")


if __name__ == "__main__":
    main()

# 动手改造：记录每次操作前后的 t+2m，并统计一次级联切断的实际次数。
