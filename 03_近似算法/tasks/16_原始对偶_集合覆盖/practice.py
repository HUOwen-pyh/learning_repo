"""Set Cover 对偶增长：构造整数覆盖和可核验 dual certificate。"""
from fractions import Fraction
from itertools import combinations
from random import Random


def primal_dual(n,sets,costs):
    y=[Fraction(0) for _ in range(n)]; picked=[]; covered=set()
    while len(covered)<n:
        e=next(e for e in range(n) if e not in covered)
        containing=[i for i,s in enumerate(sets) if e in s]
        if not containing: raise ValueError('infeasible')
        slack=lambda i: Fraction(costs[i])-sum(y[z] for z in sets[i])
        delta=min(slack(i) for i in containing); assert delta>=0
        y[e]+=delta
        tight=[i for i in containing if slack(i)==0]
        i=max(tight,key=lambda j:len(sets[j]-covered))
        if i not in picked: picked.append(i)
        covered|=sets[i]
    return picked,y


def exact(n,sets,costs):
    for budget in range(sum(costs)+1):
        for r in range(len(sets)+1):
            for c in combinations(range(len(sets)),r):
                if sum(costs[i] for i in c)==budget and len(set().union(*(sets[i] for i in c)))==n:
                    return budget
    raise ValueError


def self_test():
    rng=Random(1616)
    for n in range(1,8):
        for _ in range(50):
            sets=[{e} for e in range(n)]
            sets += [{e for e in range(n) if rng.random()<.35} for _ in range(3)]
            costs=[rng.randint(1,8) for _ in sets]
            picked,y=primal_dual(n,sets,costs); opt=exact(n,sets,costs)
            f=max(sum(e in s for s in sets) for e in range(n))
            dual=sum(y); alg=sum(costs[i] for i in picked)
            assert all(sum(y[e] for e in s)<=c for s,c in zip(sets,costs))
            assert all(sum(y[e] for e in sets[i])==costs[i] for i in picked)
            assert alg<=f*dual and dual<=opt
    print('primal-dual certificates verify ALG <= f*DUAL <= f*OPT')


if __name__=='__main__': self_test()

# 动手改造：逆序尝试删除 picked 中仍保持覆盖的集合；证明成本只降、原 dual
# 仍可行，并统计经验改善。

