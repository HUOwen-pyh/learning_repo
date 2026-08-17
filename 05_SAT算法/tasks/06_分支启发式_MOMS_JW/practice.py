"""DPLL plug-in heuristics: first, MOMS, and Jeroslow-Wang."""
from collections import Counter,defaultdict
import random,statistics

def simplify(cnf,lit):
    out=[]
    for c in cnf:
        if lit in c:continue
        r=tuple(x for x in c if x!=-lit)
        if not r:return None
        out.append(r)
    return tuple(out)

def choose(cnf,kind):
    if kind=="first":return cnf[0][0]
    if kind=="moms":
        k=min(map(len,cnf));counts=Counter(abs(l) for c in cnf if len(c)==k for l in c)
        v=max(counts,key=lambda x:(counts[x],-x));return v
    scores=defaultdict(float)
    for c in cnf:
        for l in c:scores[l]+=2.0**(-len(c))
    return max(scores,key=lambda l:(scores[l],-abs(l)))

def solve(cnf,kind,stats):
    stats["nodes"]+=1
    if not cnf:return True
    if any(not c for c in cnf):return False
    lit=choose(cnf,kind);v=abs(lit)
    for chosen in (lit,-lit):
        r=simplify(cnf,chosen)
        if r is not None and solve(r,kind,stats):return True
    return False

if __name__=="__main__":
    rng=random.Random(6);results={k:[] for k in ("first","moms","jw")}
    for _ in range(60):
        n=7;cnf=tuple(tuple(rng.choice((-1,1))*rng.randint(1,n) for _ in range(3)) for _ in range(28))
        answers=[]
        for kind in results:
            st={"nodes":0};answers.append(solve(cnf,kind,st));results[kind].append(st["nodes"])
        assert len(set(answers))==1
    for kind,values in results.items():print(kind,"median nodes",statistics.median(values))
    assert any(results["first"][i]!=results["moms"][i] for i in range(60))
    # Hands-on: add DLIS and report quartiles, not only the median.

