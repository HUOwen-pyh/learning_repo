"""两商品、两候选路径的分数最小拥塞；cut lower bound 对拍。"""
from itertools import product
from random import Random


EDGES=((0,1),(1,3),(0,2),(2,3),(1,2))
PATHS=(
    (((0,1),(1,3)), ((0,2),(2,3))),
    (((0,1),(1,2),(2,3)), ((0,2),(1,2),(1,3))),
)
DEMANDS=((0,3),(0,3))


def congestion(cap,demands,step=.02):
    best=float('inf'); best_q=None
    for a,b in product(range(round(1/step)+1),repeat=2):
        qs=(a*step,b*step); load={e:0.0 for e in EDGES}
        for i,q in enumerate(qs):
            for e in PATHS[i][0]: load[tuple(sorted(e))]+=demands[i]*q
            for e in PATHS[i][1]: load[tuple(sorted(e))]+=demands[i]*(1-q)
        rho=max(load[e]/cap[e] for e in EDGES)
        if rho<best: best,best_q=rho,qs
    return best,best_q


def cut_lower_bound(cap,demands):
    lb=0
    for mask in range(1,1<<3): # 固定顶点 3 在另一侧，避免互补重复
        S={v for v in range(3) if mask>>v&1}
        c=sum(w for e,w in cap.items() if (e[0] in S)!=(e[1] in S))
        d=sum(q for (s,t),q in zip(DEMANDS,demands) if (s in S)!=(t in S))
        if c and d: lb=max(lb,d/c)
    return lb


def self_test():
    rng=Random(2323)
    for _ in range(100):
        cap={e:rng.randint(1,6) for e in EDGES}; demands=[rng.randint(1,5),rng.randint(1,5)]
        rho,q=congestion(cap,demands); lb=cut_lower_bound(cap,demands)
        assert rho+1e-9>=lb
        assert all(0<=z<=1 for z in q)
    print('path-split congestion always respects every cut lower bound')


if __name__=='__main__': self_test()

# 动手改造：为两商品使用不同端点并自动枚举所有 simple paths；比较候选路径
# 完整/不完整时的最小拥塞。
