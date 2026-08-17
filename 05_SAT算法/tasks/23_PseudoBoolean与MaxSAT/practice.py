"""Weighted partial MaxSAT by exhaustive bound queries."""
from itertools import product

def clause_sat(c,m):return any(m[abs(l)]==(l>0) for l in c)

def optimize(hard,soft,n):
    feasible=[]
    for bits in product((False,True),repeat=n):
        m={i+1:b for i,b in enumerate(bits)}
        if not all(clause_sat(c,m) for c in hard):continue
        cost=sum(w for c,w in soft if not clause_sat(c,m))
        feasible.append((cost,m))
    return min(feasible,key=lambda x:x[0]) if feasible else None

def exists_under_bound(hard,soft,n,bound):
    answer=optimize(hard,soft,n)
    if answer is None or answer[0]>bound:return None
    # Return any model meeting bound, not necessarily the optimum.
    for bits in product((False,True),repeat=n):
        m={i+1:b for i,b in enumerate(bits)}
        if all(clause_sat(c,m) for c in hard) and sum(w for c,w in soft if not clause_sat(c,m))<=bound:
            return m

if __name__=="__main__":
    hard=((1,2),)
    soft=(((1,),3),((-1,),2),((2,),1),((-2,),4))
    optimum=optimize(hard,soft,2)
    assert optimum is not None
    cost,model=optimum
    print("optimal cost/model:",cost,model)
    assert all(clause_sat(c,model) for c in hard)
    assert exists_under_bound(hard,soft,2,cost) is not None
    assert exists_under_bound(hard,soft,2,cost-1) is None
    print("optimality evidence: feasible at",cost,"and UNSAT below",cost)
    # Hands-on: introduce explicit relaxation literals and an unweighted cardinality bound.

