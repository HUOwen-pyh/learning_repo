"""Bounded variable elimination and reverse model reconstruction."""
from itertools import product

def eliminate(cnf,var,growth_limit=0):
    pos=[c for c in cnf if var in c];neg=[c for c in cnf if -var in c]
    rest=[c for c in cnf if var not in c and -var not in c]
    resolvents=set()
    for a in pos:
        for b in neg:
            r=(set(a)-{var})|(set(b)-{-var})
            if any(-l in r for l in r):continue
            resolvents.add(frozenset(r))
    if len(resolvents)>len(pos)+len(neg)+growth_limit:return None,None
    return tuple(rest)+tuple(resolvents),(var,tuple(pos),tuple(neg))

def verify(cnf,m):
    return all(any(m[abs(l)]==(l>0) for l in c) for c in cnf)

def find_model(cnf,vars_):
    for bits in product((False,True),repeat=len(vars_)):
        m=dict(zip(vars_,bits))
        if verify(cnf,m):return m
    return None

def reconstruct(model,log):
    var,pos,neg=log
    for value in (False,True):
        candidate=dict(model);candidate[var]=value
        if verify(pos+neg,candidate):return candidate
    raise AssertionError("elimination log cannot be reconstructed")

if __name__=="__main__":
    original=tuple(map(frozenset,((1,2),(-1,3),(-2,-3),(1,-3))))
    reduced,log=eliminate(original,1,growth_limit=4)
    assert reduced is not None
    projected=find_model(reduced,[2,3])
    rebuilt=reconstruct(projected,log)
    print("reduced:",reduced,"projected:",projected,"rebuilt:",rebuilt)
    assert verify(original,rebuilt)
    # Check existential projection for every remaining assignment.
    for b2,b3 in product((False,True),repeat=2):
        rest={2:b2,3:b3}
        left=any(verify(original,rest|{1:b}) for b in (False,True))
        right=verify(reduced,rest)
        assert left==right
    explosive=tuple([frozenset((1,i)) for i in range(2,7)]+[frozenset((-1,-i)) for i in range(2,7)])
    assert eliminate(explosive,1,growth_limit=-20)==(None,None)
    # Hands-on: eliminate several variables and reconstruct logs in reverse order.

