"""Finite random-3-SAT density experiment; output is EXPERIMENT, not theorem."""
import random,statistics

def simplify(cnf,lit):
    out=[]
    for c in cnf:
        if lit in c:continue
        r=tuple(x for x in c if x!=-lit)
        if not r:return None
        out.append(r)
    return tuple(out)

def solve(cnf,stats):
    stats["nodes"]+=1
    while True:
        unit=next((c[0] for c in cnf if len(c)==1),None)
        if unit is None:break
        cnf=simplify(cnf,unit)
        if cnf is None:return False
    if not cnf:return True
    lit=cnf[0][0]
    return any(r is not None and solve(r,stats) for r in (simplify(cnf,lit),simplify(cnf,-lit)))

def random3(n,m,rng):
    return tuple(tuple(rng.choice((-1,1))*v for v in rng.sample(range(1,n+1),3)) for _ in range(m))

if __name__=="__main__":
    rng=random.Random(19);n=12;repeats=16
    rows=[]
    for alpha in (2.5,3.5,4.0,4.3,4.6,5.0,6.0):
        sat_count=0;nodes=[]
        for _ in range(repeats):
            cnf=random3(n,round(alpha*n),rng);st={"nodes":0}
            sat_count+=solve(cnf,st);nodes.append(st["nodes"])
        rows.append((alpha,sat_count/repeats,statistics.median(nodes)))
    print("EXPERIMENT n=12 repeats=16 seed=19")
    for row in rows:print("alpha=%.1f sat_rate=%.3f median_nodes=%s"%row)
    assert all(0<=rate<=1 for _,rate,_ in rows)
    # Hands-on: repeat n=16 and add bootstrap intervals for SAT rate.

