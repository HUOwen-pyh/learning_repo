"""显式路径 packing 的乘权负载均衡内核，并与离散网格 oracle 比较。"""
from itertools import product
from math import exp
from random import Random


def mw_pack(A,capacity,rounds=800,eta=.08):
    m,n=len(A),len(A[0]); load=[0.0]*m; x=[0.0]*n
    for _ in range(rounds):
        price=[exp(eta*load[e]/capacity[e]) for e in range(m)]
        j=min(range(n),key=lambda q:sum(price[e]*A[e][q]/capacity[e] for e in range(m)))
        x[j]+=1; 
        for e in range(m): load[e]+=A[e][j]
    congestion=max(load[e]/capacity[e] for e in range(m))
    return [q/congestion for q in x]


def grid_opt(A,capacity,step=.25,max_units=16):
    best=0.0
    for units in product(range(max_units+1),repeat=len(A[0])):
        x=[u*step for u in units]
        if all(sum(A[e][j]*x[j] for j in range(len(x)))<=capacity[e]+1e-9 for e in range(len(A))): best=max(best,sum(x))
    return best


def self_test():
    rng=Random(2222); ratios=[]
    for _ in range(25):
        m,n=3,3
        A=[[rng.randint(0,1) for _ in range(n)] for __ in range(m)]
        for j in range(n):
            if not any(A[e][j] for e in range(m)): A[rng.randrange(m)][j]=1
        cap=[rng.randint(1,3) for _ in range(m)]
        x=mw_pack(A,cap); alg=sum(x); opt=grid_opt(A,cap)
        assert all(sum(A[e][j]*x[j] for j in range(n))<=cap[e]+1e-8 for e in range(m))
        assert alg<=opt+.76  # grid 步长造成每变量至多 .25 的向下误差
        ratios.append(alg/opt)
    print(f'MW feasible; sampled ratio to coarse-grid OPT: min={min(ratios):.3f}, avg={sum(ratios)/len(ratios):.3f}')


if __name__=='__main__': self_test()

# 动手改造：记录每轮所选列与各资源 price；把 exp 更新换成固定价格，构造
# 固定策略严重拥塞、MW 自动分流的实例。

