"""第 02 晚：拓扑序、环判定、Kosaraju 强连通分量。"""
from __future__ import annotations
import sys
sys.stdout.reconfigure(encoding="utf-8", errors="backslashreplace")

from collections import deque


def normalize(graph: dict[str, list[str]]) -> dict[str, list[str]]:
    nodes = set(graph)
    nodes.update(v for vs in graph.values() for v in vs)
    return {u: list(dict.fromkeys(graph.get(u, []))) for u in sorted(nodes)}


def topological_sort(graph: dict[str, list[str]]) -> tuple[list[str], bool]:
    g = normalize(graph)
    indegree = {u: 0 for u in g}
    for u in g:
        for v in g[u]:
            indegree[v] += 1
    ready = deque(sorted(u for u, d in indegree.items() if d == 0))
    order: list[str] = []
    while ready:
        u = ready.popleft()
        order.append(u)
        for v in g[u]:
            indegree[v] -= 1
            if indegree[v] == 0:
                ready.append(v)
    return order, len(order) != len(g)


def strongly_connected_components(graph: dict[str, list[str]]) -> list[list[str]]:
    g = normalize(graph)
    seen: set[str] = set()
    finish: list[str] = []

    def dfs1(u: str) -> None:
        seen.add(u)
        for v in g[u]:
            if v not in seen:
                dfs1(v)
        finish.append(u)

    for u in g:
        if u not in seen:
            dfs1(u)
    reverse = {u: [] for u in g}
    for u in g:
        for v in g[u]:
            reverse[v].append(u)
    seen.clear()
    components: list[list[str]] = []

    def dfs2(u: str, component: list[str]) -> None:
        seen.add(u)
        component.append(u)
        for v in reverse[u]:
            if v not in seen:
                dfs2(v, component)

    for u in reversed(finish):
        if u not in seen:
            component: list[str] = []
            dfs2(u, component)
            components.append(sorted(component))
    return components


def condensation_edges(
    graph: dict[str, list[str]], components: list[list[str]]
) -> set[tuple[int, int]]:
    cid = {u: i for i, comp in enumerate(components) for u in comp}
    return {
        (cid[u], cid[v])
        for u, vs in normalize(graph).items()
        for v in vs
        if cid[u] != cid[v]
    }


def valid_topological(graph: dict[str, list[str]], order: list[str]) -> bool:
    pos = {u: i for i, u in enumerate(order)}
    return len(pos) == len(normalize(graph)) and all(
        pos[u] < pos[v] for u, vs in normalize(graph).items() for v in vs
    )


def main() -> None:
    dag = {"建模": ["算法"], "算法": ["测试"], "阅读": ["测试"], "测试": []}
    order, has_cycle = topological_sort(dag)
    assert not has_cycle and valid_topological(dag, order)

    graph = {
        "a": ["b"],
        "b": ["c", "d"],
        "c": ["a"],
        "d": ["e"],
        "e": ["d", "f"],
        "f": [],
        "孤立": [],
    }
    partial, has_cycle = topological_sort(graph)
    assert has_cycle and len(partial) < len(normalize(graph))
    comps = strongly_connected_components(graph)
    assert sorted(map(tuple, comps)) == sorted(
        [("a", "b", "c"), ("d", "e"), ("f",), ("孤立",)]
    )
    edges = condensation_edges(graph, comps)
    assert all(a != b for a, b in edges)
    cond_graph = {str(i): [] for i in range(len(comps))}
    for a, b in edges:
        cond_graph[str(a)].append(str(b))
    cond_order, cond_cycle = topological_sort(cond_graph)
    assert not cond_cycle and len(cond_order) == len(comps)
    print("DAG 拓扑序：", order)
    print("SCC：", comps)
    print("凝聚图边：", sorted(edges))


if __name__ == "__main__":
    main()

# 动手改造：
# 1. 改成迭代 DFS，测试 5000 点链，避免递归深度限制。
# 2. 当 Kahn 失败时，从剩余点中恢复一条具体有向环。
