"""Max-Cut：全割期望、顺序条件化 1/2 与精确 OPT。"""
from fractions import Fraction
from random import Random


def value(side,edges): return sum(w for u,v,w in edges if side[u]!=side[v])


def sequential(n,edges,order=None):
    order=list(range(n)) if order is None else order; side={}
    for v in order:
        scores=[]
        for bit in (0,1):
            scores.append((sum(w for a,b,w in edges if v in (a,b) and (a if b==v else b) in side and side[a if b==v else b]!=bit),bit))
        _,side[v]=max(scores)
    return [side[v] for v in range(n)]


def self_test():
    rng=Random(2020)
    for n in range(1,11):
        for _ in range(60):
            edges=[(u,v,rng.randint(1,9)) for u in range(n) for v in range(u+1,n) if rng.random()<.35]
            vals=[value([(mask>>v)&1 for v in range(n)],edges) for mask in range(1<<n)]
            total=sum(w for _,_,w in edges)
            assert Fraction(sum(vals),len(vals))==Fraction(total,2)
            alg=value(sequential(n,edges),edges); opt=max(vals)
            assert 2*alg>=total and 2*alg>=opt
    print('exact random-cut mean=W/2; sequential derandomization >=W/2')


if __name__=='__main__': self_test()

# 动手改造：枚举顶点顺序，找同一图上最好/最坏顺序；再接第 04 晚 1-flip，
# 断言改善后值不下降。
