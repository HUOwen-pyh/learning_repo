"""Coverage 的解析 multilinear F、离散连续贪心与保值 pipage rounding。"""
from itertools import combinations
from random import Random


def F(x,sets,weights):
    return sum(weights[e]*(1-prod(1-x[i] for i,s in enumerate(sets) if e in s)) for e in range(len(weights)))


def prod(xs):
    z=1.0
    for x in xs: z*=x
    return z


def gradient(x,sets,weights,i):
    return sum(weights[e]*prod(1-x[h] for h,s in enumerate(sets) if e in s and h!=i)
               for e in sets[i])


def continuous_greedy(sets,weights,k,steps=160):
    x=[0.0]*len(sets)
    for _ in range(steps):
        top=sorted(range(len(sets)),key=lambda i:-gradient(x,sets,weights,i))[:k]
        for i in top: x[i]+=1/steps
    return x


def pipage(x,sets,weights):
    x=x[:]
    while True:
        frac=[i for i,q in enumerate(x) if 1e-9<q<1-1e-9]
        if len(frac)<2: break
        i,j=frac[:2]; plus=min(1-x[i],x[j]); minus=min(x[i],1-x[j])
        a=x[:]; a[i]+=plus; a[j]-=plus
        b=x[:]; b[i]-=minus; b[j]+=minus
        before=F(x,sets,weights); x=max((a,b),key=lambda z:F(z,sets,weights))
        assert F(x,sets,weights)+1e-9>=before
    return {i for i,q in enumerate(x) if q>.5}


def self_test():
    rng=Random(2525)
    for m in range(3,9):
        for _ in range(30):
            n=8; sets=[{e for e in range(n) if rng.random()<.4} for __ in range(m)]; weights=[rng.randint(1,5) for _ in range(n)]
            k=rng.randint(1,min(3,m)); x=continuous_greedy(sets,weights,k)
            assert abs(sum(x)-k)<1e-8
            S=pipage(x,sets,weights); assert len(S)==k
            val=sum(weights[e] for e in set().union(*(sets[i] for i in S)))
            opt=max(sum(weights[e] for e in set().union(*(sets[i] for i in c))) for c in combinations(range(m),k))
            assert val+1e-8 >= (1-1/2.718281828-0.03)*opt
    print('continuous greedy + pipage produced cardinality-k solutions near 1-1/e')


if __name__=='__main__': self_test()

# 动手改造：输出每个 pipage 端点的 F；把 coverage 替换成显式 value oracle，
# 用枚举随机集估计 F/梯度并研究采样噪声。
