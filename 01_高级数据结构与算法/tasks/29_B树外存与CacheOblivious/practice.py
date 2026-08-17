"""第 29 晚：B-tree 插入、搜索、占用率与节点访问实验。"""

from __future__ import annotations

import sys

sys.stdout.reconfigure(encoding="utf-8")

from dataclasses import dataclass, field
import bisect
import random


@dataclass
class Node:
    leaf: bool = True
    keys: list[int] = field(default_factory=list)
    children: list["Node"] = field(default_factory=list)


class BTree:
    def __init__(self, minimum_degree: int = 3) -> None:
        if minimum_degree < 2:
            raise ValueError
        self.t = minimum_degree
        self.root = Node()

    def contains(self, key: int) -> tuple[bool, int]:
        node, visits = self.root, 0
        while True:
            visits += 1
            i = bisect.bisect_left(node.keys, key)
            if i < len(node.keys) and node.keys[i] == key:
                return True, visits
            if node.leaf:
                return False, visits
            node = node.children[i]

    def add(self, key: int) -> bool:
        if self.contains(key)[0]:
            return False
        if len(self.root.keys) == 2 * self.t - 1:
            old = self.root
            self.root = Node(leaf=False, children=[old])
            self._split_child(self.root, 0)
        self._insert_nonfull(self.root, key)
        return True

    def _split_child(self, parent: Node, index: int) -> None:
        t, full = self.t, parent.children[index]
        right = Node(leaf=full.leaf, keys=full.keys[t:])
        middle = full.keys[t - 1]
        full.keys = full.keys[: t - 1]
        if not full.leaf:
            right.children = full.children[t:]
            full.children = full.children[:t]
        parent.keys.insert(index, middle)
        parent.children.insert(index + 1, right)

    def _insert_nonfull(self, node: Node, key: int) -> None:
        if node.leaf:
            bisect.insort(node.keys, key)
            return
        i = bisect.bisect_left(node.keys, key)
        if len(node.children[i].keys) == 2 * self.t - 1:
            self._split_child(node, i)
            if key > node.keys[i]:
                i += 1
        self._insert_nonfull(node.children[i], key)

    def check(self) -> tuple[int, int]:
        leaf_depths, count = set(), 0

        def visit(node: Node, depth: int, lo: int | None, hi: int | None, is_root: bool) -> None:
            nonlocal count
            assert node.keys == sorted(node.keys) and len(node.keys) == len(set(node.keys))
            assert len(node.keys) <= 2 * self.t - 1
            if not is_root:
                assert len(node.keys) >= self.t - 1
            assert all((lo is None or lo < k) and (hi is None or k < hi) for k in node.keys)
            count += len(node.keys)
            if node.leaf:
                assert not node.children
                leaf_depths.add(depth)
            else:
                assert len(node.children) == len(node.keys) + 1
                bounds = [lo] + node.keys + [hi]
                for i, child in enumerate(node.children):
                    visit(child, depth + 1, bounds[i], bounds[i + 1], False)

        visit(self.root, 0, None, None, True)
        assert len(leaf_depths) == 1
        return count, next(iter(leaf_depths))


def main() -> None:
    rng = random.Random(29)
    for degree in (2, 4, 16):
        tree, expected = BTree(degree), set()
        for key in rng.sample(range(100_000), 4_000):
            assert tree.add(key)
            expected.add(key)
        count, height = tree.check()
        assert count == len(expected)
        probes = list(expected)[:500] + [100_001 + i for i in range(500)]
        results = [tree.contains(k) for k in probes]
        assert all(found == (k in expected) for k, (found, _) in zip(probes, results))
        print(f"t={degree}: height={height}, avg_node_visits={sum(v for _, v in results)/len(results):.2f}")


if __name__ == "__main__":
    main()

# 动手改造：给每节点设一个模拟 block id，统计一批范围查询的唯一块访问数。
