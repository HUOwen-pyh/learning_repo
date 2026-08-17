"""频率 f 集合覆盖：离散 LP 教学 oracle 与 1/f 阈值舍入。"""
from itertools import product
from random import Random


GRID=(0.0,.25,.5,.75,1.0)


def feasible(n,sets,x):
    return all(sum(x[i] for i,s in enumerate(sets) if e in s)>=1-1e-10 for e in range(n))


def grid_lp(n,sets,costs):
    best=(float('inf'),None)
    for x in product(GRID,repeat=len(sets)):
        if feasible(n,sets,x):
            val=sum(c*q for c,q in zip(costs,x))
            if val<best[0]: best=(val,x)
    return best


def exact(n,sets,costs):
    best=float('inf')
    for mask in range(1<<len(sets)):
        x=[(mask>>i)&1 for i in range(len(sets))]
        if feasible(n,sets,x): best=min(best,sum(c*q for c,q in zip(costs,x)))
    return best


def self_test():
    rng=Random(1313)
    for n in range(2,7):
        for _ in range(25):
            sets=[{e} for e in range(n)]
            sets += [{e for e in range(n) if rng.random()<.45} for _ in range(max(0,6-n))]
            sets=sets[:6]; costs=[rng.randint(1,9) for _ in sets]
            lp,x=grid_lp(n,sets,costs); opt=exact(n,sets,costs)
            f=max(sum(e in s for s in sets) for e in range(n))
            chosen=[i for i,q in enumerate(x) if q>=1/f-1e-12]
            assert all(any(e in sets[i] for i in chosen) for e in range(n))
            alg=sum(costs[i] for i in chosen)
            assert lp<=opt+1e-9 and alg<=f*lp+1e-9
    print('threshold rounding <= frequency * fractional cost')


if __name__=='__main__': self_test()

# 动手改造：用 Fraction 避免浮点；输出达到最大频率的元素及其覆盖变量和。

