"""第 11 晚：基于 split/merge 的随机 Treap。"""

from __future__ import annotations

import sys

sys.stdout.reconfigure(encoding="utf-8")

from dataclasses import dataclass
import random


@dataclass
class Node:
    key: int
    priority: float
    size: int = 1
    left: "Node | None" = None
    right: "Node | None" = None


def nsize(t: Node | None) -> int:
    return t.size if t else 0


def update(t: Node) -> None:
    t.size = 1 + nsize(t.left) + nsize(t.right)


def split(t: Node | None, key: int) -> tuple[Node | None, Node | None]:
    """返回 (< key, >= key)。"""
    if t is None:
        return None, None
    if t.key < key:
        t.right, right = split(t.right, key)
        update(t)
        return t, right
    left, t.left = split(t.left, key)
    update(t)
    return left, t


def merge(a: Node | None, b: Node | None) -> Node | None:
    if a is None:
        return b
    if b is None:
        return a
    if a.priority < b.priority:
        a.right = merge(a.right, b)
        update(a)
        return a
    b.left = merge(a, b.left)
    update(b)
    return b


def insert(t: Node | None, node: Node) -> Node:
    left, right = split(t, node.key)
    # 调用者保证键不重复。
    result = merge(merge(left, node), right)
    assert result is not None
    return result


def erase(t: Node | None, key: int) -> Node | None:
    if t is None:
        return None
    if key == t.key:
        return merge(t.left, t.right)
    if key < t.key:
        t.left = erase(t.left, key)
    else:
        t.right = erase(t.right, key)
    update(t)
    return t


def inorder(t: Node | None) -> list[int]:
    return inorder(t.left) + [t.key] + inorder(t.right) if t else []


def check(t: Node | None, lo: int | None = None, hi: int | None = None) -> int:
    if t is None:
        return 0
    assert (lo is None or lo < t.key) and (hi is None or t.key < hi)
    assert t.left is None or t.priority <= t.left.priority
    assert t.right is None or t.priority <= t.right.priority
    total = 1 + check(t.left, lo, t.key) + check(t.right, t.key, hi)
    assert t.size == total
    return total


def main() -> None:
    rng, root, expected = random.Random(11), None, set()
    for _ in range(500):
        key = rng.randrange(2_000)
        if rng.random() < 0.65 and key not in expected:
            root = insert(root, Node(key, rng.random()))
            expected.add(key)
        else:
            root = erase(root, key)
            expected.discard(key)
        check(root)
        assert inorder(root) == sorted(expected)
    left, right = split(root, 1_000)
    assert all(x < 1_000 for x in inorder(left)) and all(x >= 1_000 for x in inorder(right))
    root = merge(left, right)
    assert inorder(root) == sorted(expected)
    print(f"通过：随机操作后保留 {len(expected)} 个键，split/merge 可逆。")


if __name__ == "__main__":
    main()

# 动手改造：利用 size 实现第 k 小查询，并与 sorted(expected)[k] 差分。
