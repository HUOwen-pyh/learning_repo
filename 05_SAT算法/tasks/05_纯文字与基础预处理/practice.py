"""Fixed-point unit/pure preprocessing with reconstruction checks."""
from itertools import product
import random

def normalize(clauses):
    out=[]
    for clause in clauses:
        c=frozenset(clause)
        if any(-l in c for l in c):continue
        out.append(c)
    return tuple(out)

def assign(clauses,lit):
    out=[]
    for c in clauses:
        if lit in c:continue
        r=c-{-lit}
        if not r:return None
        out.append(r)
    return tuple(out)

def preprocess(clauses):
    clauses=normalize(clauses); log={}
    while True:
        if any(not c for c in clauses):return None,log
        if not clauses:return clauses,log
        units=[next(iter(c)) for c in clauses if len(c)==1]
        all_lits=set().union(*clauses)
        pures=[l for l in all_lits if -l not in all_lits]
        candidates=units or pures
        if not candidates:return clauses,log
        lit=candidates[0];var=abs(lit)
        if var in log and log[var]!=(lit>0):return None,log
        log[var]=lit>0;clauses=assign(clauses,lit)
        if clauses is None:return None,log

def verify(clauses,model):
    return all(any(model[abs(l)]==(l>0) for l in c) for c in clauses)

def models(clauses,n,fixed=None):
    fixed={} if fixed is None else fixed
    free=[v for v in range(1,n+1) if v not in fixed]
    for bits in product((False,True),repeat=len(free)):
        m=dict(fixed);m.update(zip(free,bits))
        if verify(clauses,m):yield m

if __name__ == "__main__":
    rng=random.Random(5)
    for _ in range(100):
        n=5
        raw=tuple(tuple(rng.choice((-1,1))*rng.randint(1,n) for _ in range(3))
                  for _ in range(8))
        original=normalize(raw)
        reduced,log=preprocess(original)
        before=next(models(original,n),None)
        after=None if reduced is None else next(models(reduced,n,log),None)
        assert (before is None)==(after is None)
        if after is not None:assert verify(original,after)
    assert normalize(((1,-1,2),))==()
    print("100 preprocessing cases preserved satisfiability and reconstructed models.")
    # Hands-on: add subsumption and count removed clauses per rule.

