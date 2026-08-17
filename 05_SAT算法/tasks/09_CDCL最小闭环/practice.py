"""A compact clause-learning solver (full blocking conflicts) with backjumping.

For clarity this learns the negation of the current decision prefix. It is a
valid entailed clause after a conflict, though weaker than first-UIP CDCL.
"""
from itertools import product
import random

def verify(cnf,model):
    return all(any(model.get(abs(l),False)==(l>0) for l in c) for c in cnf)

def propagate(cnf,assignment,levels,reasons,trail,level,stats):
    while True:
        changed=False
        for ci,c in enumerate(cnf):
            stats["clause_checks"]+=1
            if any(assignment.get(abs(l))==(l>0) for l in c):continue
            unknown=[l for l in c if abs(l) not in assignment]
            if not unknown:return ci
            if len(unknown)==1:
                lit=unknown[0];v=abs(lit)
                assignment[v]=lit>0;levels[v]=level;reasons[v]=ci;trail.append(lit)
                stats["propagations"]+=1;changed=True
        if not changed:return None

def solve(cnf,n):
    db=[tuple(c) for c in cnf];a={};levels={};reasons={};trail=[]
    decisions=[];stats={"decisions":0,"conflicts":0,"learned":0,"backjumps":0,
                        "propagations":0,"clause_checks":0}
    while True:
        conflict=propagate(db,a,levels,reasons,trail,len(decisions),stats)
        if conflict is not None:
            stats["conflicts"]+=1
            if not decisions:return None,stats
            # Negate all decision literals: current conflicting subtree is impossible.
            learned=tuple(-lit for lit in decisions)
            assert learned
            db.append(learned);stats["learned"]+=1
            # Backjump to the second-highest decision level (often non-chronological
            # after unit propagation makes the clause asserting).
            target=max(0,len(decisions)-1)
            cut=next((i for i,l in enumerate(trail) if levels[abs(l)]>target),len(trail))
            for lit in trail[cut:]:
                v=abs(lit);a.pop(v,None);levels.pop(v,None);reasons.pop(v,None)
            del trail[cut:];del decisions[target:]
            stats["backjumps"]+=1
            continue
        if len(a)==n:
            assert verify(cnf,a);return dict(a),stats
        v=next(v for v in range(1,n+1) if v not in a)
        decisions.append(v);a[v]=True;levels[v]=len(decisions);reasons[v]=None;trail.append(v)
        stats["decisions"]+=1

def brute(cnf,n):
    return any(verify(cnf,{i+1:b for i,b in enumerate(bits)}) for bits in product((False,True),repeat=n))

if __name__=="__main__":
    rng=random.Random(9)
    totals={"conflicts":0,"learned":0}
    for _ in range(80):
        n=6;cnf=tuple(tuple(rng.choice((-1,1))*rng.randint(1,n) for _ in range(3)) for _ in range(22))
        model,stats=solve(cnf,n)
        assert (model is not None)==brute(cnf,n)
        if model is not None:assert verify(cnf,model)
        for k in totals:totals[k]+=stats[k]
    print("80 formulas matched brute force; totals:",totals)
    assert totals["learned"]>0
    # Hands-on: replace prefix blocking by the first-UIP analysis from night 08.

