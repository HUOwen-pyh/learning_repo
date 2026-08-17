"""第 9 晚：维护 height 与 size 的 AVL 插入。"""

from __future__ import annotations

import sys

sys.stdout.reconfigure(encoding="utf-8")

from dataclasses import dataclass
import math


@dataclass
class Node:
    key: int
    height: int = 1
    size: int = 1
    left: "Node | None" = None
    right: "Node | None" = None


def height(x: Node | None) -> int:
    return x.height if x else 0


def size(x: Node | None) -> int:
    return x.size if x else 0


def update(x: Node) -> None:
    x.height = 1 + max(height(x.left), height(x.right))
    x.size = 1 + size(x.left) + size(x.right)


def rotate_right(y: Node) -> Node:
    x = y.left
    assert x is not None
    y.left, x.right = x.right, y
    update(y)
    update(x)
    return x


def rotate_left(x: Node) -> Node:
    y = x.right
    assert y is not None
    x.right, y.left = y.left, x
    update(x)
    update(y)
    return y


def insert(root: Node | None, key: int) -> Node:
    if root is None:
        return Node(key)
    if key < root.key:
        root.left = insert(root.left, key)
    elif key > root.key:
        root.right = insert(root.right, key)
    else:
        return root
    update(root)
    balance = height(root.left) - height(root.right)
    if balance > 1:
        assert root.left
        if key > root.left.key:
            root.left = rotate_left(root.left)
        return rotate_right(root)
    if balance < -1:
        assert root.right
        if key < root.right.key:
            root.right = rotate_right(root.right)
        return rotate_left(root)
    return root


def check(x: Node | None, lo: int | None = None, hi: int | None = None) -> tuple[int, int]:
    if x is None:
        return 0, 0
    assert (lo is None or lo < x.key) and (hi is None or x.key < hi)
    lh, ls = check(x.left, lo, x.key)
    rh, rs = check(x.right, x.key, hi)
    assert abs(lh - rh) <= 1
    assert x.height == 1 + max(lh, rh) and x.size == 1 + ls + rs
    return x.height, x.size


def main() -> None:
    for seq in ([3, 2, 1], [1, 2, 3], [3, 1, 2], [1, 3, 2]):
        root = None
        for key in seq:
            root = insert(root, key)
        assert root.key == 2
        check(root)
    root = None
    for key in range(1, 1_001):
        root = insert(root, key)
    h, n = check(root)
    assert n == 1_000 and h < 2 * math.log2(n + 1)
    print(f"通过：有序插入 n={n} 后高度={h}。")


if __name__ == "__main__":
    main()

# 动手改造：给旋转函数加入计数器，比较有序与随机插入的每次插入旋转数。
