"""3CNF 的 FGLSS 风格局部配置冲突图：MIS == MaxSAT 值。"""
from functools import lru_cache
from itertools import product
from random import Random


def local_configs(clause):
    vars_=tuple(v for v,_ in clause); out=[]
    for bits in product((False,True),repeat=3):
        a=dict(zip(vars_,bits))
        if any(a[v]==pos for v,pos in clause): out.append(a)
    return out


def fglss(clauses):
    vertices=[]
    for ci,c in enumerate(clauses):
        for a in local_configs(c): vertices.append((ci,a))
    n=len(vertices); nbr=[0]*n
    for i in range(n):
        ci,a=vertices[i]
        for j in range(i+1,n):
            cj,b=vertices[j]
            conflict=ci==cj or any(v in b and b[v]!=bit for v,bit in a.items())
            if conflict: nbr[i]|=1<<j; nbr[j]|=1<<i
    return nbr


def mis_size(nbr):
    @lru_cache(None)
    def go(mask):
        if not mask:return 0
        v=(mask&-mask).bit_length()-1; without=mask&~(1<<v)
        return max(go(without),1+go(without&~nbr[v]))
    return go((1<<len(nbr))-1)


def maxsat(n,clauses):
    return max(sum(any(bits[v]==pos for v,pos in c) for c in clauses) for bits in product((False,True),repeat=n))


def self_test():
    rng=Random(2828)
    for n in range(3,6):
        for _ in range(12):
            clauses=[]
            for __ in range(4):
                vs=rng.sample(range(n),3); clauses.append(tuple((v,bool(rng.getrandbits(1))) for v in vs))
            nbr=fglss(clauses)
            assert mis_size(nbr)==maxsat(n,clauses)
    print('FGLSS consistency graph: alpha(G) equals maximum satisfiable clauses')


if __name__=='__main__': self_test()

# 动手改造：让 verifier 的随机串/clause 带有 Fraction 权重，实现最大权独立集，
# 并与加权 MaxSAT 枚举对拍。

