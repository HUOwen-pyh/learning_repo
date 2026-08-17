"""小规模 Christofides：Prim、最小完美匹配、Euler 多重图、shortcut。"""
from functools import lru_cache
from itertools import permutations
from math import hypot
from random import Random


def metric(points):
    return [[hypot(x-a, y-b) for a, b in points] for x, y in points]


def prim_edges(d):
    n=len(d); key=[float('inf')]*n; par=[-1]*n; used=[False]*n; key[0]=0
    for _ in range(n):
        u=min((i for i in range(n) if not used[i]), key=key.__getitem__); used[u]=True
        for v in range(n):
            if not used[v] and d[u][v]<key[v]: key[v],par[v]=d[u][v],u
    return [(par[v],v) for v in range(1,n)]


def min_pairing(vertices, d):
    vertices=tuple(vertices)
    @lru_cache(None)
    def solve(rem):
        if not rem: return 0.0, ()
        u=rem[0]; best=(float('inf'),())
        for j in range(1,len(rem)):
            v=rem[j]; rest=rem[1:j]+rem[j+1:]
            cost,pairs=solve(rest); cand=(d[u][v]+cost, ((u,v),)+pairs)
            if cand[0]<best[0]: best=cand
        return best
    return solve(vertices)


def euler_shortcut(n, edges):
    adj=[[] for _ in range(n)]
    for eid,(u,v) in enumerate(edges): adj[u].append((v,eid)); adj[v].append((u,eid))
    used=set(); stack=[0]; circuit=[]
    while stack:
        u=stack[-1]
        while adj[u] and adj[u][-1][1] in used: adj[u].pop()
        if not adj[u]: circuit.append(stack.pop())
        else:
            v,eid=adj[u].pop(); used.add(eid); stack.append(v)
    assert len(used)==len(edges)
    seen=set(); order=[]
    for v in reversed(circuit):
        if v not in seen: seen.add(v); order.append(v)
    return order


def christofides(d):
    tree=prim_edges(d); deg=[0]*len(d)
    for u,v in tree: deg[u]+=1; deg[v]+=1
    odd=[v for v in range(len(d)) if deg[v]%2]
    _,matching=min_pairing(odd,d)
    return euler_shortcut(len(d), tree+list(matching))


def cost(t,d): return sum(d[t[i]][t[(i+1)%len(t)]] for i in range(len(t)))
def exact(d): return min(cost((0,)+p,d) for p in permutations(range(1,len(d))))


def self_test():
    rng=Random(909)
    for n in range(2,9):
        for _ in range(15):
            d=metric([(rng.randrange(40),rng.randrange(40)) for _ in range(n)])
            tour=christofides(d); assert sorted(tour)==list(range(n))
            assert cost(tour,d)<=1.5*exact(d)+1e-8
    print('Christofides <= 3/2 OPT on all oracle-checked metrics')


if __name__=='__main__': self_test()

# 动手改造：统计 double-tree 与 Christofides 在同一批实例的平均/最坏比值；
# 再缓存 matching DP 的状态数，和奇点数联系起来。

