"""Subsumption, self-subsuming resolution, and blocked clauses."""
from itertools import product

def normalize(cnf):return tuple(frozenset(c) for c in cnf)

def subsume(cnf):
    return tuple(c for i,c in enumerate(cnf) if not any(d<c for j,d in enumerate(cnf) if i!=j))

def ssr_pair(a,b):
    # If a\{l} subset b and -l in b, remove -l from b.
    for l in a:
        if -l in b and (a-{l}) <= (b-{-l}):
            return b-{-l}
    return b

def resolvent_tautological(a,b,l):
    r=(a-{l})|(b-{-l})
    return any(-x in r for x in r)

def blocked(cnf,index,l):
    c=cnf[index]
    return l in c and all(resolvent_tautological(c,d,l) for j,d in enumerate(cnf)
                          if j!=index and -l in d)

def models(cnf,n):
    out=set()
    for bits in product((False,True),repeat=n):
        m={i+1:b for i,b in enumerate(bits)}
        if all(any(m[abs(l)]==(l>0) for l in c) for c in cnf):out.add(bits)
    return out

if __name__=="__main__":
    cnf=normalize(((1,2),(1,2,3),(-1,2,3)))
    reduced=subsume(cnf)
    assert models(cnf,3)==models(reduced,3)
    a=frozenset((1,2));b=frozenset((-1,2,3))
    shortened=ssr_pair(a,b)
    assert shortened==frozenset((2,3))
    assert models((a,b),3)==models((a,shortened),3)
    bce=normalize(((1,2),(-1,-2)))
    assert blocked(bce,0,1)
    without=bce[1:]
    assert bool(models(bce,2))==bool(models(without,2))
    print("subsumption and SSR preserved models; BCE preserved satisfiability.")
    # Hands-on: record the blocking literal and reconstruct a model of the original.
