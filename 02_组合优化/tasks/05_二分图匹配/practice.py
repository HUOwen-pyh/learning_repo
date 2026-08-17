"""第 05 晚：Hopcroft-Karp 与 Kőnig 最小顶点覆盖证书。"""
from __future__ import annotations
import sys
sys.stdout.reconfigure(encoding="utf-8", errors="backslashreplace")

from collections import deque
import math


def hopcroft_karp(
    left: list[str], right: list[str], adj: dict[str, list[str]]
) -> tuple[dict[str, str | None], dict[str, str | None]]:
    pair_l: dict[str, str | None] = {u: None for u in left}
    pair_r: dict[str, str | None] = {v: None for v in right}
    dist: dict[str, float] = {}

    def bfs() -> bool:
        q: deque[str] = deque()
        found = False
        for u in left:
            if pair_l[u] is None:
                dist[u] = 0
                q.append(u)
            else:
                dist[u] = math.inf
        while q:
            u = q.popleft()
            for v in adj.get(u, []):
                mate = pair_r[v]
                if mate is None:
                    found = True
                elif dist[mate] == math.inf:
                    dist[mate] = dist[u] + 1
                    q.append(mate)
        return found

    def dfs(u: str) -> bool:
        for v in adj.get(u, []):
            mate = pair_r[v]
            if mate is None or (dist[mate] == dist[u] + 1 and dfs(mate)):
                pair_l[u], pair_r[v] = v, u
                return True
        dist[u] = math.inf
        return False

    while bfs():
        for u in left:
            if pair_l[u] is None:
                dfs(u)
    return pair_l, pair_r


def min_vertex_cover(
    left: list[str],
    adj: dict[str, list[str]],
    pair_l: dict[str, str | None],
    pair_r: dict[str, str | None],
) -> tuple[set[str], set[str]]:
    z_left = {u for u in left if pair_l[u] is None}
    z_right: set[str] = set()
    q = deque(z_left)
    while q:
        u = q.popleft()
        for v in adj.get(u, []):
            if pair_l[u] == v or v in z_right:
                continue  # 左到右只走非匹配边
            z_right.add(v)
            mate = pair_r[v]
            if mate is not None and mate not in z_left:
                z_left.add(mate)
                q.append(mate)
    return set(left) - z_left, z_right


def main() -> None:
    left = ["A", "B", "C", "D", "E"]
    right = ["1", "2", "3", "4"]
    adj = {
        "A": ["1", "2"],
        "B": ["1"],
        "C": ["2", "3"],
        "D": ["3", "4"],
        "E": ["3"],
    }
    pair_l, pair_r = hopcroft_karp(left, right, adj)
    matching = {(u, v) for u, v in pair_l.items() if v is not None}
    assert len({u for u, _ in matching}) == len(matching)
    assert len({v for _, v in matching}) == len(matching)
    assert all(v in adj[u] for u, v in matching)
    cover_l, cover_r = min_vertex_cover(left, adj, pair_l, pair_r)
    assert all(u in cover_l or v in cover_r for u in left for v in adj.get(u, []))
    assert len(cover_l) + len(cover_r) == len(matching) == 4
    assert any(pair_l[u] is None for u in left)  # 鸽巢原理：不存在左侧完美匹配
    print("最大匹配：", sorted(matching))
    print("最小顶点覆盖：L", sorted(cover_l), "R", sorted(cover_r))
    print("primal=dual=", len(matching))


if __name__ == "__main__":
    main()

# 动手改造：
# 1. 随机生成 n<=7 的二分图，用穷举匹配核对算法。
# 2. 给边加权，研究为何 Hopcroft-Karp 不再保证最大权。
