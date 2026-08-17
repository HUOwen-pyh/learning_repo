"""第 10 晚：左倾红黑树插入与全不变量检查。"""

from __future__ import annotations

import sys

sys.stdout.reconfigure(encoding="utf-8")

from dataclasses import dataclass
import math
import random

RED, BLACK = True, False


@dataclass
class Node:
    key: int
    color: bool = RED
    left: "Node | None" = None
    right: "Node | None" = None


def is_red(x: Node | None) -> bool:
    return x is not None and x.color == RED


def rotate_left(h: Node) -> Node:
    x = h.right
    assert x and is_red(x)
    h.right, x.left = x.left, h
    x.color, h.color = h.color, RED
    return x


def rotate_right(h: Node) -> Node:
    x = h.left
    assert x and is_red(x)
    h.left, x.right = x.right, h
    x.color, h.color = h.color, RED
    return x


def flip_colors(h: Node) -> None:
    assert h.left and h.right
    h.color = not h.color
    h.left.color = not h.left.color
    h.right.color = not h.right.color


def _insert(h: Node | None, key: int) -> Node:
    if h is None:
        return Node(key)
    if key < h.key:
        h.left = _insert(h.left, key)
    elif key > h.key:
        h.right = _insert(h.right, key)
    if is_red(h.right) and not is_red(h.left):
        h = rotate_left(h)
    if is_red(h.left) and h.left and is_red(h.left.left):
        h = rotate_right(h)
    if is_red(h.left) and is_red(h.right):
        flip_colors(h)
    return h


def insert(root: Node | None, key: int) -> Node:
    root = _insert(root, key)
    root.color = BLACK
    return root


def check(x: Node | None, lo: int | None = None, hi: int | None = None) -> tuple[int, int, int]:
    if x is None:
        return 1, 0, 0  # 空叶黑高为 1
    assert (lo is None or lo < x.key) and (hi is None or x.key < hi)
    assert not is_red(x.right)
    assert not (is_red(x) and (is_red(x.left) or is_red(x.right)))
    lb, lh, ln = check(x.left, lo, x.key)
    rb, rh, rn = check(x.right, x.key, hi)
    assert lb == rb
    return lb + (x.color == BLACK), 1 + max(lh, rh), 1 + ln + rn


def main() -> None:
    for values in (list(range(1_000)), random.Random(10).sample(range(10_000), 1_000)):
        root = None
        for key in values:
            root = insert(root, key)
        assert root.color == BLACK
        black_height, height, n = check(root)
        assert n == 1_000 and height <= 2 * math.ceil(math.log2(n + 1))
        print(f"n={n}, height={height}, black_height={black_height}：通过")


if __name__ == "__main__":
    main()

# 动手改造：输出 Graphviz DOT 文本，用红/黑边观察 2-3 树对应关系。
