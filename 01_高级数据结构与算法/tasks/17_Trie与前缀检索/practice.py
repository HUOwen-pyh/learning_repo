"""第 17 晚：带子树词数的 Trie。"""

from __future__ import annotations

import sys

sys.stdout.reconfigure(encoding="utf-8")

from dataclasses import dataclass, field
import random
import string


@dataclass
class Node:
    children: dict[str, "Node"] = field(default_factory=dict)
    terminal: bool = False
    subtree_words: int = 0


class Trie:
    def __init__(self) -> None:
        self.root = Node()

    def contains(self, word: str) -> bool:
        node = self.root
        for ch in word:
            if ch not in node.children:
                return False
            node = node.children[ch]
        return node.terminal

    def add(self, word: str) -> bool:
        if self.contains(word):
            return False
        node, path = self.root, [self.root]
        for ch in word:
            node = node.children.setdefault(ch, Node())
            path.append(node)
        node.terminal = True
        for x in path:
            x.subtree_words += 1
        return True

    def discard(self, word: str) -> bool:
        node, path = self.root, [self.root]
        for ch in word:
            if ch not in node.children:
                return False
            node = node.children[ch]
            path.append(node)
        if not node.terminal:
            return False
        node.terminal = False
        for x in path:
            x.subtree_words -= 1
        for parent, ch, child in zip(path, word, path[1:]):
            if child.subtree_words == 0:
                del parent.children[ch]
                break
        return True

    def prefix_count(self, prefix: str) -> int:
        node = self.root
        for ch in prefix:
            if ch not in node.children:
                return 0
            node = node.children[ch]
        return node.subtree_words

    def complete(self, prefix: str) -> list[str]:
        node = self.root
        for ch in prefix:
            if ch not in node.children:
                return []
            node = node.children[ch]
        out: list[str] = []

        def visit(x: Node, suffix: str) -> None:
            if x.terminal:
                out.append(prefix + suffix)
            for ch in sorted(x.children):
                visit(x.children[ch], suffix + ch)

        visit(node, "")
        return out


def main() -> None:
    rng, trie, reference = random.Random(17), Trie(), set()
    universe = ["".join(rng.choice(string.ascii_lowercase[:8]) for _ in range(rng.randrange(0, 9))) for _ in range(500)]
    for _ in range(1_000):
        word = rng.choice(universe)
        if rng.random() < 0.6:
            assert trie.add(word) == (word not in reference)
            reference.add(word)
        else:
            assert trie.discard(word) == (word in reference)
            reference.discard(word)
    for prefix in ("", "a", "ab", "face"):
        expected = sorted(x for x in reference if x.startswith(prefix))
        assert trie.prefix_count(prefix) == len(expected)
        assert trie.complete(prefix) == expected
    print(f"通过：{len(reference)} 个词；空前缀列出全集。")


if __name__ == "__main__":
    main()

# 动手改造：complete(prefix, limit) 到达 limit 后停止 DFS。
