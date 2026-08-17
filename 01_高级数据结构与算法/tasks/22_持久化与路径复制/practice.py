"""第 22 晚：不可变节点 + 路径复制的持久化线段树。"""

from __future__ import annotations

import sys

sys.stdout.reconfigure(encoding="utf-8")

from dataclasses import dataclass
import random


@dataclass(frozen=True)
class Node:
    total: int
    left: "Node | None" = None
    right: "Node | None" = None


def build(a: list[int], lo: int = 0, hi: int | None = None) -> Node:
    hi = len(a) if hi is None else hi
    if hi - lo == 1:
        return Node(a[lo])
    mid = (lo + hi) // 2
    left, right = build(a, lo, mid), build(a, mid, hi)
    return Node(left.total + right.total, left, right)


def update(node: Node, index: int, value: int, lo: int, hi: int) -> Node:
    if hi - lo == 1:
        return Node(value)
    assert node.left and node.right
    mid = (lo + hi) // 2
    if index < mid:
        left, right = update(node.left, index, value, lo, mid), node.right
    else:
        left, right = node.left, update(node.right, index, value, mid, hi)
    return Node(left.total + right.total, left, right)


def query(node: Node, left: int, right: int, lo: int, hi: int) -> int:
    if right <= lo or hi <= left:
        return 0
    if left <= lo and hi <= right:
        return node.total
    assert node.left and node.right
    mid = (lo + hi) // 2
    return query(node.left, left, right, lo, mid) + query(node.right, left, right, mid, hi)


def collect_ids(node: Node) -> set[int]:
    ids, stack = set(), [node]
    while stack:
        x = stack.pop()
        ids.add(id(x))
        if x.left:
            stack.extend([x.left, x.right])  # type: ignore[list-item]
    return ids


def main() -> None:
    n, rng = 128, random.Random(22)
    original = [rng.randrange(-20, 21) for _ in range(n)]
    roots, arrays = [build(original)], [original]
    for _ in range(80):
        base = rng.randrange(len(roots))  # 从任意旧版本分叉
        i, value = rng.randrange(n), rng.randrange(-100, 101)
        a = arrays[base].copy()
        a[i] = value
        roots.append(update(roots[base], i, value, 0, n))
        arrays.append(a)
    for root, a in zip(roots, arrays):
        for _ in range(5):
            l, r = sorted((rng.randrange(n + 1), rng.randrange(n + 1)))
            assert query(root, l, r, 0, n) == sum(a[l:r])
    shared = len(collect_ids(roots[0]) & collect_ids(roots[1]))
    assert shared > 0
    print(f"通过：{len(roots)} 个可分叉版本；首个更新与原版共享 {shared} 个节点。")


if __name__ == "__main__":
    main()

# 动手改造：实现两个版本在区间 [l,r) 的和之差，不创建新节点。
