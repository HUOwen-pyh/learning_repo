"""Metric UFL 的 Mettu–Plaxton radius ordering 与设施子集 oracle。"""
from itertools import combinations
from math import hypot
from random import Random


def dist(a,b): return hypot(a[0]-b[0],a[1]-b[1])


def radius(facility,clients,opening):
    ds=sorted(dist(facility,c) for c in clients); prefix=0.0
    for k,d in enumerate(ds,1):
        prefix+=d
        next_d=ds[k] if k<len(ds) else float('inf')
        r=(opening+prefix)/k
        if r<=next_d+1e-12 and r>=d-1e-12: return r
    raise AssertionError


def solve(facilities,clients,opening):
    rs=[radius(f,clients,c) for f,c in zip(facilities,opening)]; opened=[]
    for i in sorted(range(len(facilities)),key=lambda z:rs[z]):
        if all(dist(facilities[i],facilities[h])>2*rs[i]+1e-12 for h in opened): opened.append(i)
    return opened


def cost(chosen,facilities,clients,opening):
    return sum(opening[i] for i in chosen)+sum(min(dist(c,facilities[i]) for i in chosen) for c in clients)


def exact(facilities,clients,opening):
    return min(cost(c,facilities,clients,opening) for r in range(1,len(facilities)+1) for c in combinations(range(len(facilities)),r))


def self_test():
    rng=Random(1919)
    for nf in range(1,8):
        for _ in range(50):
            fs=[(rng.randrange(30),rng.randrange(30)) for _ in range(nf)]
            cs=[(rng.randrange(30),rng.randrange(30)) for _ in range(7)]
            op=[rng.randint(1,30) for _ in fs]
            chosen=solve(fs,cs,op); alg=cost(chosen,fs,cs,op); opt=exact(fs,cs,op)
            assert chosen and alg<=3*opt+1e-8
    print('radius-based UFL solution <= 3*OPT on oracle-checked metrics')


if __name__=='__main__': self_test()

# 动手改造：输出每个设施的 r 与“因谁被挡”；验证被挡者到挡者距离 <=2r。
