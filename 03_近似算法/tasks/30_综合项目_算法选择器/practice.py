"""可审计近似算法选择器：三类问题、证书、前提检查与随机 CI。"""
from itertools import combinations
from math import hypot
from random import Random


def solve(instance):
    kind=instance['kind']
    if kind=='vertex_cover':
        n,edges=instance['n'],instance['edges']; used=set(); matching=[]
        for u,v in edges:
            if not (0<=u<n and 0<=v<n and u!=v): raise ValueError('invalid edge')
            if u not in used and v not in used: used|={u,v}; matching.append((u,v))
        assert all(u in used or v in used for u,v in edges)
        return {'algorithm':'maximal-matching endpoints','guarantee':'cost <= 2 OPT','value':len(used),'lower_bound':len(matching),'solution':sorted(used)}
    if kind=='k_center':
        pts,k=instance['points'],instance['k']
        if not 1<=k<=len(pts): raise ValueError('k out of range')
        C=[0]
        while len(C)<k:
            C.append(max(range(len(pts)),key=lambda x:min(hypot(pts[x][0]-pts[c][0],pts[x][1]-pts[c][1]) for c in C)))
        r=max(min(hypot(pts[x][0]-pts[c][0],pts[x][1]-pts[c][1]) for c in C) for x in range(len(pts)))
        return {'algorithm':'farthest-first','guarantee':'radius <= 2 OPT','value':r,'solution':C,'verified':'Euclidean metric'}
    if kind=='maximum_coverage':
        sets,k=instance['sets'],instance['k']; C=[]; covered=set()
        for _ in range(min(k,len(sets))):
            i=max((i for i in range(len(sets)) if i not in C),key=lambda i:len(sets[i]-covered)); C.append(i); covered|=sets[i]
        return {'algorithm':'marginal greedy','guarantee':'value >= (1-1/e) OPT','value':len(covered),'solution':C,'verified':'monotone coverage'}
    raise ValueError('unsupported problem kind')


def self_test():
    rng=Random(3030)
    for n in range(2,10):
        edges=[e for e in combinations(range(n),2) if rng.random()<.3]
        r=solve({'kind':'vertex_cover','n':n,'edges':edges})
        opt=min(len(S) for q in range(n+1) for S in combinations(range(n),q) if all(u in S or v in S for u,v in edges))
        assert r['value']<=2*opt
        pts=[(rng.randrange(20),rng.randrange(20)) for _ in range(n)]; k=rng.randint(1,min(3,n))
        r=solve({'kind':'k_center','points':pts,'k':k})
        opt=min(max(min(hypot(pts[x][0]-pts[c][0],pts[x][1]-pts[c][1]) for c in C) for x in range(n)) for C in combinations(range(n),k))
        assert r['value']<=2*opt+1e-9
        sets=[{x for x in range(n) if rng.random()<.4} for _ in range(n)]; r=solve({'kind':'maximum_coverage','sets':sets,'k':k})
        opt=max(len(set().union(*(sets[i] for i in C))) for C in combinations(range(n),k))
        assert r['value']+1e-9>=(1-(1-1/k)**k)*opt
    print('all selector branches passed exact-oracle CI')
    print(solve({'kind':'vertex_cover','n':4,'edges':[(0,1),(1,2),(2,3)]}))


if __name__=='__main__': self_test()

# 动手改造：新增 metric_tsp 分支：先 O(n^3) 检查三角不等式，再调用第 08 晚
# double-tree；报告 MST lower bound，并让非度量输入明确抛错。
