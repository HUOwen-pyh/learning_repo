"""第 30 晚综合项目：线性化的并发流式索引。仅用标准库。"""

from __future__ import annotations

import sys

sys.stdout.reconfigure(encoding="utf-8")

from dataclasses import dataclass, field
import hashlib
import heapq
import math
import random
import threading


def hashes(key: str, count: int, modulo: int, person: bytes) -> list[int]:
    raw = hashlib.blake2b(key.encode(), digest_size=16, person=person[:16]).digest()
    a, b = int.from_bytes(raw[:8], "little"), int.from_bytes(raw[8:], "little") | 1
    return [(a + i * b) % modulo for i in range(count)]


class Bloom:
    def __init__(self, capacity: int, p: float = 0.01) -> None:
        self.m = math.ceil(-capacity * math.log(p) / math.log(2) ** 2)
        self.k = max(1, round(self.m / capacity * math.log(2)))
        self.bits = bytearray((self.m + 7) // 8)

    def add(self, key: str) -> None:
        for position in hashes(key, self.k, self.m, b"capstone-bloom"):
            self.bits[position // 8] |= 1 << (position % 8)

    def contains(self, key: str) -> bool:
        return all(self.bits[p // 8] & 1 << (p % 8) for p in hashes(key, self.k, self.m, b"capstone-bloom"))


class CountMin:
    def __init__(self, width: int = 512, depth: int = 5) -> None:
        self.width, self.depth = width, depth
        self.table = [[0] * width for _ in range(depth)]

    def add(self, key: str) -> None:
        for row, column in enumerate(hashes(key, self.depth, self.width, b"capstone-cms")):
            self.table[row][column] += 1

    def estimate(self, key: str) -> int:
        return min(self.table[row][column] for row, column in enumerate(hashes(key, self.depth, self.width, b"capstone-cms")))


@dataclass
class TrieNode:
    children: dict[str, "TrieNode"] = field(default_factory=dict)
    distinct_below: int = 0


class PrefixTrie:
    def __init__(self) -> None:
        self.root = TrieNode()

    def add_distinct(self, key: str) -> None:
        node = self.root
        node.distinct_below += 1
        for ch in key:
            node = node.children.setdefault(ch, TrieNode())
            node.distinct_below += 1

    def count(self, prefix: str) -> int:
        node = self.root
        for ch in prefix:
            if ch not in node.children:
                return 0
            node = node.children[ch]
        return node.distinct_below


@dataclass(frozen=True)
class Snapshot:
    total_events: int
    distinct_keys: int
    top: tuple[tuple[str, int], ...]


class ConcurrentStreamIndex:
    """所有公开操作以同一把锁为线性化边界。"""

    def __init__(self, expected_distinct: int = 10_000) -> None:
        self._lock = threading.Lock()
        self._exact: dict[str, int] = {}
        self._bloom = Bloom(expected_distinct)
        self._cms = CountMin()
        self._trie = PrefixTrie()
        self._heap: list[tuple[int, str]] = []  # (-observed_count, key)，含过期条目
        self._total = 0

    def add(self, key: str) -> None:
        if not isinstance(key, str):
            raise TypeError("key must be str")
        with self._lock:  # 线性化点位于临界区内
            first = key not in self._exact
            self._exact[key] = self._exact.get(key, 0) + 1
            self._total += 1
            self._bloom.add(key)
            self._cms.add(key)
            if first:
                self._trie.add_distinct(key)
            heapq.heappush(self._heap, (-self._exact[key], key))

    def possibly_seen(self, key: str) -> bool:
        with self._lock:
            return self._bloom.contains(key)

    def estimate(self, key: str) -> int:
        with self._lock:
            return self._cms.estimate(key)

    def prefix_distinct(self, prefix: str) -> int:
        with self._lock:
            return self._trie.count(prefix)

    def _top_locked(self, k: int) -> tuple[tuple[str, int], ...]:
        # heap 中同一键有历史条目；弹掉顶部过期项，再在副本上取不同键。
        while self._heap and -self._heap[0][0] != self._exact[self._heap[0][1]]:
            heapq.heappop(self._heap)
        copy, result, used = self._heap.copy(), [], set()
        heapq.heapify(copy)
        while copy and len(result) < k:
            neg, key = heapq.heappop(copy)
            if key not in used and -neg == self._exact[key]:
                used.add(key)
                result.append((key, -neg))
        return tuple(result)

    def snapshot(self, top_k: int = 5) -> Snapshot:
        with self._lock:
            return Snapshot(self._total, len(self._exact), self._top_locked(top_k))

    def exact_copy_for_test(self) -> dict[str, int]:
        with self._lock:
            return self._exact.copy()


def main() -> None:
    rng = random.Random(30)
    batches: list[list[str]] = []
    reference: dict[str, int] = {}
    for worker in range(4):
        batch = []
        local = random.Random(rng.randrange(1 << 30))
        for _ in range(2_500):
            key = f"topic/{local.randrange(25):02d}/item/{local.randrange(120):03d}"
            batch.append(key)
            reference[key] = reference.get(key, 0) + 1
        batches.append(batch)

    index = ConcurrentStreamIndex(expected_distinct=4_000)
    threads = [threading.Thread(target=lambda xs=xs: [index.add(x) for x in xs]) for xs in batches]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

    exact = index.exact_copy_for_test()
    assert exact == reference
    snap = index.snapshot(10)
    assert snap.total_events == 10_000 and snap.distinct_keys == len(reference)
    assert all(index.possibly_seen(key) for key in reference)  # Bloom 无假阴性
    assert all(index.estimate(key) >= count for key, count in reference.items())
    for prefix in ("topic/00", "topic/12", "topic/"):
        assert index.prefix_distinct(prefix) == sum(key.startswith(prefix) for key in reference)
    expected_top = sorted(reference.items(), key=lambda item: (-item[1], item[0]))[:10]
    assert sorted(snap.top, key=lambda item: (-item[1], item[0])) == expected_top
    print(f"通过：4 线程、{snap.total_events} 事件、{snap.distinct_keys} 个键；top3={snap.top[:3]}")


if __name__ == "__main__":
    main()

# 动手改造：按稳定哈希分成 4 个 shard；为全局 snapshot 明确一致性契约。
