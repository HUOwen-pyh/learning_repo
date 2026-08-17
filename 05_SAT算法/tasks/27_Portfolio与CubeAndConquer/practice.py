"""Cube coverage and sequential simulation of cube-and-conquer."""
from itertools import product
import random,statistics

def cubes(depth):
    return [tuple((i+1 if bit else -(i+1)) for i,bit in enumerate(bits))
            for bits in product((False,True),repeat=depth)]

def covered(assignment,cube):
    return all(assignment[abs(l)]==(l>0) for l in cube)

def verify(cnf,m):return all(any(m[abs(l)]==(l>0) for l in c) for c in cnf)

def solve_under(cnf,n,cube):
    fixed={abs(l):l>0 for l in cube};nodes=0
    free=[v for v in range(1,n+1) if v not in fixed]
    for bits in product((False,True),repeat=len(free)):
        nodes+=1;m=fixed|dict(zip(free,bits))
        if verify(cnf,m):return m,nodes
    return None,nodes

if __name__=="__main__":
    n=7;depth=3;partition=cubes(depth)
    for bits in product((False,True),repeat=n):
        m={i+1:b for i,b in enumerate(bits)}
        assert sum(covered(m,c) for c in partition)==1
    rng=random.Random(27)
    cnf=tuple(tuple(rng.choice((-1,1))*rng.randint(1,n) for _ in range(3)) for _ in range(30))
    results=[solve_under(cnf,n,c) for c in partition]
    aggregate=next((m for m,_ in results if m is not None),None)
    brute,_=solve_under(cnf,n,())
    assert (aggregate is None)==(brute is None)
    if aggregate:assert verify(cnf,aggregate)
    loads=[nodes for _,nodes in results]
    print("cubes:",len(partition),"load median/max:",statistics.median(loads),max(loads))
    # Hands-on: make overlapping cubes and verify at-least-one coverage plus duplicate work.

