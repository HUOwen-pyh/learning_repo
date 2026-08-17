"""第 6 晚：二项最小堆，重点是 meld 的二进制进位。"""

from __future__ import annotations

import sys

sys.stdout.reconfigure(encoding="utf-8")

from dataclasses import dataclass, field
import heapq
import random


@dataclass
class Node:
    key: int
    children: list["Node"] = field(default_factory=list)

    @property
    def degree(self) -> int:
        return len(self.children)


def link(a: Node, b: Node) -> Node:
    assert a.degree == b.degree
    if b.key < a.key:
        a, b = b, a
    a.children.append(b)  # 新孩子的阶最大，列表阶数为 0..k-1
    return a


class BinomialHeap:
    def __init__(self) -> None:
        self.roots: dict[int, Node] = {}
        self.n = 0

    def push(self, key: int) -> None:
        other = BinomialHeap()
        other.roots[0] = Node(key)
        other.n = 1
        self.meld(other)

    def meld(self, other: "BinomialHeap") -> None:
        buckets: dict[int, list[Node]] = {}
        for degree, root in list(self.roots.items()) + list(other.roots.items()):
            buckets.setdefault(degree, []).append(root)
        self.roots = {}
        carry: Node | None = None
        degree = 0
        while buckets or carry is not None:
            nodes = buckets.pop(degree, [])
            if carry is not None:
                nodes.append(carry)
                carry = None
            if len(nodes) == 1:
                self.roots[degree] = nodes[0]
            elif len(nodes) == 2:
                carry = link(nodes[0], nodes[1])
            elif len(nodes) == 3:
                self.roots[degree] = nodes[0]
                carry = link(nodes[1], nodes[2])
            assert len(nodes) <= 3
            degree += 1
        self.n += other.n
        other.roots.clear()
        other.n = 0
        self.check()

    def pop(self) -> int:
        if not self.roots:
            raise IndexError("pop from empty heap")
        degree, root = min(self.roots.items(), key=lambda item: item[1].key)
        del self.roots[degree]
        child_heap = BinomialHeap()
        child_heap.roots = {child.degree: child for child in root.children}
        child_heap.n = (1 << degree) - 1
        self.n -= 1 << degree
        answer = root.key
        self.meld(child_heap)
        return answer

    def check(self) -> None:
        assert self.n == sum(1 << d for d in self.roots)
        for degree, root in self.roots.items():
            assert root.degree == degree
            stack = [root]
            while stack:
                node = stack.pop()
                assert [c.degree for c in node.children] == list(range(node.degree))
                assert all(node.key <= c.key for c in node.children)
                stack.extend(node.children)


def main() -> None:
    rng = random.Random(6)
    left, right, reference = BinomialHeap(), BinomialHeap(), []
    for _ in range(200):
        x = rng.randrange(10_000)
        (left if rng.random() < 0.5 else right).push(x)
        heapq.heappush(reference, x)
    left.meld(right)
    assert right.n == 0
    assert [left.pop() for _ in range(left.n)] == [heapq.heappop(reference) for _ in range(len(reference))]
    print("通过：200 个元素 meld 后按序弹出；源堆已清空。")


if __name__ == "__main__":
    main()

# 动手改造：缓存最小根，使 peek_min 为 O(1)，列出每个更新点。
