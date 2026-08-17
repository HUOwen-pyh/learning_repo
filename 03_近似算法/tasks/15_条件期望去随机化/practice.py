"""Max-3SAT 的条件期望去随机化：确定性达到随机 7/8 基线。"""
from fractions import Fraction
from itertools import product
from random import Random


def clause_prob(clause,assignment):
    unknown=set()
    for var,positive in clause:
        if var in assignment:
            if assignment[var]==positive: return Fraction(1)
        else: unknown.add(var)
    return Fraction(0) if not unknown else 1-Fraction(1,2**len(unknown))


def expected(clauses,assignment): return sum((clause_prob(c,assignment) for c in clauses),Fraction())


def derandomize(n,clauses):
    a={}; prev=expected(clauses,a)
    for v in range(n):
        choices=[]
        for bit in (False,True):
            b={**a,v:bit}; choices.append((expected(clauses,b),bit))
        now,bit=max(choices); a[v]=bit
        assert now>=prev; prev=now
    return a,int(prev)


def exact(n,clauses):
    return max(sum(any(bits[v]==pos for v,pos in c) for c in clauses)
               for bits in product((False,True),repeat=n))


def self_test():
    rng=Random(1515)
    for n in range(3,11):
        for _ in range(40):
            clauses=[]
            for __ in range(24):
                vs=rng.sample(range(n),3)
                clauses.append(tuple((v,bool(rng.getrandbits(1))) for v in vs))
            a,val=derandomize(n,clauses)
            actual=sum(any(a[v]==pos for v,pos in c) for c in clauses)
            assert val==actual and actual*8>=7*len(clauses)
            assert actual<=exact(n,clauses)
    print('conditional expectation deterministically preserves the 7/8 baseline')


if __name__=='__main__': self_test()

# 动手改造：每步打印 E[Z|prefix, x=False/True]；再支持 1/2/3 混合长度子句，
# 初始下界改为各 clause 的 (1-2^-k) 之和。
