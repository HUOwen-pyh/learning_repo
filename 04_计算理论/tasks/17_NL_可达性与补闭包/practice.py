"""第17晚：逐层可达集合与“不同顶点计数”不变量。"""
import random

def reachable_layers(n, edges, source):
    current = {source}
    layers = [frozenset(current)]
    for _ in range(n - 1):
        expanded = current | {v for u,v in edges if u in current}
        layers.append(frozenset(expanded))
        if expanded == current:
            break
        current = expanded
    return layers

def dfs_reachable(n, edges, source):
    adjacency = {u:set() for u in range(n)}
    for u,v in edges:
        adjacency[u].add(v)
    seen, stack = set(), [source]
    while stack:
        u = stack.pop()
        if u not in seen:
            seen.add(u); stack.extend(adjacency[u]-seen)
    return seen

if __name__ == "__main__":
    rng = random.Random(17)
    n = 12
    edges = {(u,v) for u in range(n) for v in range(n) if rng.random() < .10}
    layers = reachable_layers(n,edges,0)
    counts = [len(s) for s in layers]
    final = set(layers[-1])
    print("counts of vertices at distance <= k:",counts)
    print("unreachable certificate targets:",sorted(set(range(n))-final))
    assert counts == sorted(counts)
    assert final == dfs_reachable(n,edges,0)
    assert all(not any((u,v) in edges and u in final for u in final) for v in set(range(n))-final)
    # 动手改造：计“路径条数”并找一个与“顶点数”分歧最早的图。
