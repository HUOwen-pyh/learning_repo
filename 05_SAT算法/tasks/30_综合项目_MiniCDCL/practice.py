"""Integrated mini SAT laboratory: DIMACS, DPLL, model and UNSAT evidence."""
from itertools import product
import json,random,time

def parse(text):
    lines=[l.strip() for l in text.splitlines() if l.strip() and not l.lstrip().startswith("c")]
    head=lines.pop(0).split();assert head[:2]==["p","cnf"]
    n,m=int(head[2]),int(head[3]);clauses=[]
    for line in lines:
        xs=list(map(int,line.split()));assert xs[-1]==0
        clauses.append(tuple(xs[:-1]))
    assert len(clauses)==m;return n,tuple(clauses)

def verify(cnf,m):return all(any(m.get(abs(l),False)==(l>0) for l in c) for c in cnf)

def dpll(cnf,n,a,stats):
    stats["nodes"]+=1
    while True:
        if not cnf:return dict(a)
        if any(not c for c in cnf):return None
        unit=next((c[0] for c in cnf if len(c)==1),None)
        if unit is None:break
        v=abs(unit);value=unit>0
        if v in a and a[v]!=value:return None
        a[v]=value;stats["propagations"]+=1
        cnf=tuple(tuple(x for x in c if x!=-unit) for c in cnf if unit not in c)
    v=next(v for v in range(1,n+1) if v not in a)
    stats["decisions"]+=1
    for value in (True,False):
        lit=v if value else -v;child=dict(a);child[v]=value
        reduced=tuple(tuple(x for x in c if x!=-lit) for c in cnf if lit not in c)
        model=dpll(reduced,n,child,stats)
        if model is not None:return model
    return None

def exhaustive_unsat(cnf,n):
    checked=0
    for bits in product((False,True),repeat=n):
        checked+=1;m={i+1:b for i,b in enumerate(bits)}
        if verify(cnf,m):return False,checked
    return True,checked

def experiment(name,text):
    n,cnf=parse(text);stats={"nodes":0,"decisions":0,"propagations":0}
    start=time.perf_counter();model=dpll(cnf,n,{},stats);elapsed=(time.perf_counter()-start)*1000
    if model is not None:
        assert verify(cnf,model);evidence={"kind":"MODEL","assignment":model}
    else:
        unsat,checked=exhaustive_unsat(cnf,n);assert unsat
        evidence={"kind":"COMPLETE_ENUMERATION","assignments_checked":checked}
    return {"name":name,"variables":n,"clauses":len(cnf),"status":"SAT" if model else "UNSAT",
            **stats,"elapsed_ms":round(elapsed,3),"evidence":evidence}

if __name__=="__main__":
    sat_text="p cnf 3 3\n1 2 0\n-1 3 0\n-2 3 0\n"
    unsat_text="p cnf 1 2\n1 0\n-1 0\n"
    report={"python":"3.11+","seed":30,"labels":{"algorithm":"INVARIANT/THEOREM",
             "timing":"EXPERIMENT","timeout":"UNKNOWN"},"runs":[experiment("sat",sat_text),experiment("unsat",unsat_text)]}
    rng=random.Random(30)
    for i in range(20):
        n=5;cnf=tuple(tuple(rng.choice((-1,1))*rng.randint(1,n) for _ in range(3)) for _ in range(14))
        text=f"p cnf {n} {len(cnf)}\n"+"\n".join(" ".join(map(str,c))+" 0" for c in cnf)+"\n"
        run=experiment(f"random-{i}",text)
        assert run["status"] in ("SAT","UNSAT")
    print(json.dumps(report,ensure_ascii=True,indent=2))
    assert report["runs"][0]["status"]=="SAT" and report["runs"][1]["status"]=="UNSAT"
    # Hands-on: integrate first-UIP CDCL and RUP logging; keep this solver as differential oracle.

