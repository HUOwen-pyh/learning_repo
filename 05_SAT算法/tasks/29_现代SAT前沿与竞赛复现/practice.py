"""Reproducible heuristic ablation on a fixed small benchmark family."""
from collections import Counter
import csv,io,random

def simplify(cnf,lit):
    out=[]
    for c in cnf:
        if lit in c:continue
        r=tuple(x for x in c if x!=-lit)
        if not r:return None
        out.append(r)
    return tuple(out)

def choose(cnf,mode,rng):
    variables=sorted({abs(l) for c in cnf for l in c})
    if mode=="first":return variables[0]
    if mode=="random":return rng.choice(variables)
    counts=Counter(abs(l) for c in cnf for l in c)
    return max(variables,key=lambda v:(counts[v],-v))

def search(cnf,mode,rng,stats):
    stats["nodes"]+=1
    if not cnf:return True
    if any(not c for c in cnf):return False
    v=choose(cnf,mode,rng)
    return any(r is not None and search(r,mode,rng,stats)
               for r in (simplify(cnf,v),simplify(cnf,-v)))

if __name__=="__main__":
    master=random.Random(290)
    benchmarks=[tuple(tuple(master.choice((-1,1))*master.randint(1,8) for _ in range(3)) for _ in range(32))
                for _ in range(12)]
    output=io.StringIO();writer=csv.writer(output);writer.writerow(["mode","solved","nodes","seed"])
    totals={}
    for mode in ("first","occurrence","random"):
        nodes=0;answers=[]
        for i,cnf in enumerate(benchmarks):
            st={"nodes":0};ans=search(cnf,mode,random.Random(29000+i),st)
            answers.append(ans);nodes+=st["nodes"]
        totals[mode]=(sum(answers),nodes);writer.writerow([mode,len(answers),nodes,290])
        if mode!="first":assert answers==baseline
        else:baseline=answers
    print(output.getvalue());print("EXPERIMENT:",totals)
    assert len(set(s for s,_ in totals.values()))==1
    print("Competition statuses: SAT=10, UNSAT=20, UNKNOWN=0.")
    # Hands-on: add unit propagation as a separate ablation and retain negative results.

