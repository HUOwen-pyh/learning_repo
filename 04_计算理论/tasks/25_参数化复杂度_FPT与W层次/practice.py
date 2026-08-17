"""第25晚：Vertex Cover 的 2^k 分支与 Buss 风格核化。"""
from itertools import combinations
import random

def normalize(edges):
    return frozenset(tuple(sorted(e)) for e in edges if e[0] != e[1])

def branch_vc(edges,k,stats):
    stats["nodes"] += 1
    if not edges:
        return frozenset()
    if k == 0:
        return None
    u,v = next(iter(edges))
    for chosen in (u,v):
        reduced = frozenset(e for e in edges if chosen not in e)
        rest = branch_vc(reduced,k-1,stats)
        if rest is not None:
            return rest | {chosen}
    return None

def kernelize(edges,k):
    edges, forced = set(edges), set()
    while edges:
        degree = {}
        for u,v in edges:
            degree[u] = degree.get(u,0)+1; degree[v] = degree.get(v,0)+1
        high = next((v for v,d in degree.items() if d > k),None)
        if high is None:
            break
        forced.add(high); k -= 1
        if k < 0:
            return None,None,None
        edges = {e for e in edges if high not in e}
    if len(edges) > k*k:
        return None,None,None
    return frozenset(edges),k,frozenset(forced)

def solve_fpt(edges,k):
    kernel,newk,forced = kernelize(edges,k)
    if kernel is None:
        return None,{"nodes":0}
    stats = {"nodes":0}
    rest = branch_vc(kernel,newk,stats)
    return (None if rest is None else rest|forced),stats

def brute_exists(n,edges,k):
    return any(all(u in s or v in s for u,v in edges)
               for size in range(k+1) for s in map(set,combinations(range(n),size)))

if __name__ == "__main__":
    rng = random.Random(25)
    for _ in range(30):
        n = 9
        edges = normalize((u,v) for u in range(n) for v in range(u+1,n) if rng.random()<.25)
        for k in range(5):
            cover,stats = solve_fpt(edges,k)
            assert (cover is not None) == brute_exists(n,edges,k)
            if cover is not None:
                assert len(cover)<=k and all(u in cover or v in cover for u,v in edges)
    print("30 random graphs × 5 k values matched brute force.")
    # 动手改造：累计分支节点，按 k 汇总中位数，并与 n^k 枚举区分。

