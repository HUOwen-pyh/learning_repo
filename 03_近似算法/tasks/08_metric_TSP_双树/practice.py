"""Metric TSP double-tree/preorder 2-近似及排列 oracle。"""
from itertools import permutations
from math import hypot
from random import Random


def distances(points):
    return [[hypot(x-a, y-b) for a, b in points] for x, y in points]


def prim_tree(d):
    n, parent = len(d), [-1] * len(d)
    key, used = [float("inf")] * n, [False] * n
    key[0] = 0.0
    for _ in range(n):
        u = min((i for i in range(n) if not used[i]), key=key.__getitem__)
        used[u] = True
        for v in range(n):
            if not used[v] and d[u][v] < key[v]:
                key[v], parent[v] = d[u][v], u
    return parent, sum(key)


def preorder_tour(d):
    parent, mst = prim_tree(d)
    children = [[] for _ in d]
    for v in range(1, len(d)):
        children[parent[v]].append(v)
    order = []
    def dfs(u):
        order.append(u)
        for v in children[u]: dfs(v)
    dfs(0)
    return order, mst


def tour_cost(order, d):
    return sum(d[order[i]][order[(i + 1) % len(order)]] for i in range(len(order)))


def exact_tsp(d):
    return min(tour_cost((0,) + p, d) for p in permutations(range(1, len(d))))


def self_test():
    rng = Random(808)
    for n in range(2, 9):
        for _ in range(20):
            pts = [(rng.randrange(30), rng.randrange(30)) for _ in range(n)]
            d = distances(pts)
            order, mst = preorder_tour(d)
            alg, opt = tour_cost(order, d), exact_tsp(d)
            assert alg <= 2 * mst + 1e-8
            assert mst <= opt + 1e-8
            assert alg <= 2 * opt + 1e-8
    print("double-tree <= 2*MST <= 2*OPT on all metric instances")


if __name__ == "__main__": self_test()

# 动手改造：在 DFS 时按“离当前点最近的孩子”排序，比较经验值；证明保证仍是 2。

