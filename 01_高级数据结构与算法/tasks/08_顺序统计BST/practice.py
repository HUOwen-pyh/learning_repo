"""第 8 晚：支持重复键的顺序统计 BST。"""

from __future__ import annotations

import sys

sys.stdout.reconfigure(encoding="utf-8")

from dataclasses import dataclass
import bisect
import random


@dataclass
class Node:
    key: int
    count: int = 1
    size: int = 1
    left: "Node | None" = None
    right: "Node | None" = None


def size(node: Node | None) -> int:
    return node.size if node else 0


def insert(node: Node | None, key: int) -> Node:
    if node is None:
        return Node(key)
    if key < node.key:
        node.left = insert(node.left, key)
    elif key > node.key:
        node.right = insert(node.right, key)
    else:
        node.count += 1
    node.size = node.count + size(node.left) + size(node.right)
    return node


def select(node: Node | None, k: int) -> int:
    if node is None or not 0 <= k < node.size:
        raise IndexError(k)
    left = size(node.left)
    if k < left:
        return select(node.left, k)
    if k < left + node.count:
        return node.key
    return select(node.right, k - left - node.count)


def rank(node: Node | None, key: int) -> int:
    """严格小于 key 的元素数。"""
    total = 0
    while node:
        if key <= node.key:
            node = node.left
        else:
            total += size(node.left) + node.count
            node = node.right
    return total


def check(node: Node | None, lo: int | None = None, hi: int | None = None) -> int:
    if node is None:
        return 0
    assert (lo is None or lo < node.key) and (hi is None or node.key < hi)
    total = node.count + check(node.left, lo, node.key) + check(node.right, node.key, hi)
    assert node.size == total and node.count > 0
    return total


def main() -> None:
    rng, root, reference = random.Random(8), None, []
    for _ in range(400):
        key = rng.randrange(-50, 51)
        root = insert(root, key)
        bisect.insort(reference, key)
    check(root)
    assert [select(root, k) for k in range(len(reference))] == reference
    for key in range(-60, 61):
        assert rank(root, key) == bisect.bisect_left(reference, key)
    print(f"通过：size={root.size if root else 0}，rank/select 与排序列表一致。")


if __name__ == "__main__":
    main()

# 动手改造：用 rank(hi+1)-rank(lo) 实现闭区间计数，并处理整数边界。
