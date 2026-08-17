"""Steiner Tree 的终端 metric-closure MST 2-近似与边子集 oracle。"""
from itertools import combinations
from random import Random


def connected(n,edges,chosen,terminals):
    adj=[[] for _ in range(n)]
    for i,(u,v,w) in enumerate(edges):
        if i in chosen: adj[u].append(v); adj[v].append(u)
    seen={terminals[0]}; stack=list(seen)
    while stack:
        u=stack.pop()
        for v in adj[u]:
            if v not in seen: seen.add(v); stack.append(v)
    return all(t in seen for t in terminals)


def exact(n,edges,terminals):
    best=float('inf')
    for mask in range(1<<len(edges)):
        cost=sum(w for i,(_,_,w) in enumerate(edges) if mask>>i&1)
        if cost<best and connected(n,edges,{i for i in range(len(edges)) if mask>>i&1},terminals): best=cost
    return best


def approx(n,edges,terminals):
    inf=10**9; d=[[inf]*n for _ in range(n)]; nxt=[[None]*n for _ in range(n)]
    for i in range(n): d[i][i]=0
    for eid,(u,v,w) in enumerate(edges):
        if w<d[u][v]: d[u][v]=d[v][u]=w; nxt[u][v]=(v,eid); nxt[v][u]=(u,eid)
    for k in range(n):
        for i in range(n):
            for j in range(n):
                if d[i][k]+d[k][j]<d[i][j]: d[i][j]=d[i][k]+d[k][j]; nxt[i][j]=nxt[i][k]
    parent={t:t for t in terminals}
    def root(a):
        while parent[a]!=a: parent[a]=parent[parent[a]]; a=parent[a]
        return a
    pairs=sorted((d[a][b],a,b) for a,b in combinations(terminals,2)); chosen_pairs=[]
    for _,a,b in pairs:
        ra,rb=root(a),root(b)
        if ra!=rb: parent[ra]=rb; chosen_pairs.append((a,b))
    used=set()
    for a,b in chosen_pairs:
        while a!=b:
            a2,eid=nxt[a][b]; used.add(eid); a=a2
    return sum(edges[i][2] for i in used),used


def self_test():
    rng=Random(1717)
    for n in range(3,8):
        for _ in range(40):
            edges=[(i,i+1,rng.randint(1,9)) for i in range(n-1)]
            extra=list(combinations(range(n),2)); rng.shuffle(extra)
            present={(u,v) for u,v,_ in edges}
            for u,v in extra[:max(0,8-len(edges))]:
                if (u,v) not in present: edges.append((u,v,rng.randint(1,9)))
            terminals=sorted(rng.sample(range(n),rng.randint(2,n)))
            alg,used=approx(n,edges,terminals); opt=exact(n,edges,terminals)
            assert connected(n,edges,used,terminals) and alg<=2*opt
    print('terminal metric-MST expansion <= 2*Steiner OPT')


if __name__=='__main__': self_test()

# 动手改造：在 used 的子图上删环（Kruskal），验证成本不增；输出 Steiner 点。

