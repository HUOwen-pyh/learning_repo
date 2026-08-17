"""concave-over-modular 单调次模函数：公理枚举、贪心与精确解。"""
from itertools import combinations
from math import sqrt
from random import Random


def make_value(features,weights):
    def f(S): return sum(w*sqrt(sum(row[e] for e in S)) for row,w in zip(features,weights))
    return f


def greedy(n,k,f):
    S=set()
    for _ in range(k): S.add(max((e for e in range(n) if e not in S),key=lambda e:f(S|{e})-f(S)))
    return S


def check_submodular(n,f):
    subsets=[{i for i in range(n) if mask>>i&1} for mask in range(1<<n)]
    for A in subsets:
        for B in subsets:
            assert f(A)+f(B)+1e-10>=f(A|B)+f(A&B)


def self_test():
    rng=Random(2424)
    for n in range(2,9):
        features=[[rng.randint(0,5) for _ in range(n)] for __ in range(3)]; weights=[1,2,3]
        f=make_value(features,weights); check_submodular(n,f)
        for k in range(1,min(4,n)+1):
            S=greedy(n,k,f); opt=max(f(set(c)) for c in combinations(range(n),k))
            bound=1-(1-1/k)**k
            assert f(S)+1e-9>=bound*opt
    print('submodularity axioms and greedy finite-k guarantee verified')


if __name__=='__main__': self_test()

# 动手改造：实现 lazy greedy 并计数 value-oracle 调用；用平方替换 sqrt，打印
# 第一个违反次模不等式的 A,B。

