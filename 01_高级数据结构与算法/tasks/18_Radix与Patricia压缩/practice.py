"""第 18 晚：字符串边标签的压缩 Radix Tree。"""

from __future__ import annotations

import sys

sys.stdout.reconfigure(encoding="utf-8")

from dataclasses import dataclass, field


@dataclass
class Node:
    terminal: bool = False
    edges: dict[str, tuple[str, "Node"]] = field(default_factory=dict)


def lcp_length(a: str, b: str) -> int:
    i = 0
    while i < min(len(a), len(b)) and a[i] == b[i]:
        i += 1
    return i


class RadixTree:
    def __init__(self) -> None:
        self.root = Node()

    def add(self, word: str) -> bool:
        node, rest = self.root, word
        while rest:
            edge = node.edges.get(rest[0])
            if edge is None:
                node.edges[rest[0]] = (rest, Node(terminal=True))
                return True
            label, child = edge
            common = lcp_length(rest, label)
            if common == len(label):
                node, rest = child, rest[common:]
                continue
            middle = Node()
            node.edges[rest[0]] = (label[:common], middle)
            old_suffix = label[common:]
            middle.edges[old_suffix[0]] = (old_suffix, child)
            new_suffix = rest[common:]
            if new_suffix:
                middle.edges[new_suffix[0]] = (new_suffix, Node(terminal=True))
            else:
                middle.terminal = True
            return True
        if node.terminal:
            return False
        node.terminal = True
        return True

    def contains(self, word: str) -> bool:
        node, rest = self.root, word
        while rest:
            edge = node.edges.get(rest[0])
            if edge is None:
                return False
            label, node = edge
            if not rest.startswith(label):
                return False
            rest = rest[len(label):]
        return node.terminal

    def words(self) -> list[str]:
        out: list[str] = []

        def visit(node: Node, prefix: str) -> None:
            if node.terminal:
                out.append(prefix)
            for label, child in node.edges.values():
                visit(child, prefix + label)

        visit(self.root, "")
        return sorted(out)

    def check(self) -> int:
        nodes = 0

        def visit(node: Node, is_root: bool) -> None:
            nonlocal nodes
            nodes += 1
            assert len(node.edges) == len({label[0] for label, _ in node.edges.values()})
            for first, (label, child) in node.edges.items():
                assert label and first == label[0]
                visit(child, False)
            if not is_root and not node.terminal:
                assert len(node.edges) >= 2

        visit(self.root, True)
        return nodes


def main() -> None:
    words = ["", "a", "an", "ant", "ante", "anti", "answer", "banana", "band", "bandana"]
    tree = RadixTree()
    for word in words:
        assert tree.add(word)
        assert not tree.add(word)
    assert tree.words() == sorted(words)
    assert all(tree.contains(w) for w in words)
    assert not any(tree.contains(w) for w in ["ans", "ban", "bandit", "z"])
    nodes = tree.check()
    print(f"通过：{len(words)} 个词仅使用 {nodes} 个显式节点。")


if __name__ == "__main__":
    main()

# 动手改造：实现删除，并在非终止节点只剩一个孩子时合并两条边。
