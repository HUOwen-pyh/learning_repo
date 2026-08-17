"""Vertex Cover FPT 分支 + learning-augmented Max-Cut 安全组合器。"""
from itertools import combinations
from random import Random


def fpt_vc(edges,k):
    edges=tuple(edges)
    if not edges:return set()
    if k==0:return None
    u,v=edges[0]
    for x in (u,v):
        rest=tuple((a,b) for a,b in edges if x not in (a,b)); ans=fpt_vc(rest,k-1)
        if ans is not None:return ans|{x}
    return None


def exact_vc(n,edges):
    for k in range(n+1):
        for S in combinations(range(n),k):
            if all(u in S or v in S for u,v in edges):return set(S)


def cut(side,edges):return sum(w for u,v,w in edges if side[u]!=side[v])


def baseline(n,edges):
    side={}
    for v in range(n):
        side[v]=max((0,1),key=lambda bit:sum(w for a,b,w in edges if v in (a,b) and (a if b==v else b) in side and side[a if b==v else b]!=bit))
    return [side[v] for v in range(n)]


def self_test():
    rng=Random(2929)
    for n in range(1,11):
        graph=[e for e in combinations(range(n),2) if rng.random()<.35]; opt=exact_vc(n,graph)
        for k in range(n+1): assert (fpt_vc(graph,k) is not None)==(len(opt)<=k)
        wedges=[(u,v,rng.randint(1,9)) for u,v in combinations(range(n),2) if rng.random()<.35]
        cuts=[[(mask>>v)&1 for v in range(n)] for mask in range(1<<n)]; true=max(cuts,key=lambda s:cut(s,wedges))
        pred=[b^(rng.random()<.25) for b in true]; base=baseline(n,wedges)
        chosen=max((pred,base),key=lambda s:cut(s,wedges)); optval=cut(true,wedges)
        assert cut(chosen,wedges)>=cut(base,wedges) and cut(chosen,wedges)>=cut(pred,wedges)
        assert 2*cut(chosen,wedges)>=optval
    print('FPT decisions exact; prediction wrapper is robust and prediction-consistent')


if __name__=='__main__': self_test()

# 动手改造：加入 deg(v)>k 的 Buss 规则和 |E|>k^2 拒绝规则，统计递归节点；
# 对预测翻转率 0..1 画 chosen/base/pred 三条平均质量曲线。

