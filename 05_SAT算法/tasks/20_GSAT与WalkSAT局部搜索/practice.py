"""WalkSAT on planted instances; budget exhaustion returns UNKNOWN."""
import random

def satisfied(clause,a):return any(a[abs(l)]==(l>0) for l in clause)
def verify(cnf,a):return all(satisfied(c,a) for c in cnf)

def planted_3sat(n,m,rng):
    planted={v:rng.choice((False,True)) for v in range(1,n+1)};clauses=[]
    while len(clauses)<m:
        vars_=rng.sample(range(1,n+1),3)
        clause=[rng.choice((-1,1))*v for v in vars_]
        if satisfied(clause,planted):clauses.append(tuple(clause))
    return tuple(clauses),planted

def walksat(cnf,n,rng,max_flips=5000,noise=.4):
    a={v:rng.choice((False,True)) for v in range(1,n+1)}
    for step in range(max_flips+1):
        bad=[c for c in cnf if not satisfied(c,a)]
        if not bad:return "SAT",a,step
        if step==max_flips:break
        clause=rng.choice(bad)
        if rng.random()<noise:v=abs(rng.choice(clause))
        else:
            def break_count(v):
                b=dict(a);b[v]=not b[v]
                return sum(not satisfied(c,b) for c in cnf)
            v=min(map(abs,clause),key=lambda x:(break_count(x),x))
        a[v]=not a[v]
    return "UNKNOWN",None,max_flips

if __name__=="__main__":
    rng=random.Random(20);cnf,planted=planted_3sat(30,120,rng)
    successes=0
    for _ in range(12):
        status,model,steps=walksat(cnf,30,rng,3000,.4)
        if status=="SAT":
            successes+=1;assert verify(cnf,model)
        else:assert model is None
    print("12 restarts, verified successes:",successes)
    assert successes>0 and verify(cnf,planted)
    unsat=((1,),(-1,))
    assert walksat(unsat,1,rng,20)[0]=="UNKNOWN"
    # Hands-on: maintain clause true-counts incrementally and differential-test each flip.

