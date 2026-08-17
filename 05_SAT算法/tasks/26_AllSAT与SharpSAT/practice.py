"""AllSAT, projected blocking, and exact model counting."""
from itertools import product

def sat(cnf,m):return all(any(m[abs(l)]==(l>0) for l in c) for c in cnf)

def solve(cnf,n):
    return next(({i+1:b for i,b in enumerate(bits)} for bits in product((False,True),repeat=n)
                 if sat(cnf,{i+1:b for i,b in enumerate(bits)})),None)

def allsat(cnf,n,projection=None):
    projection=list(range(1,n+1)) if projection is None else list(projection)
    db=list(cnf);answers=[]
    while True:
        model=solve(tuple(db),n)
        if model is None:return answers
        key=tuple(model[v] for v in projection);answers.append((key,model))
        db.append(tuple(-v if model[v] else v for v in projection))

def count_branch(cnf,n,var=1):
    if any(not c for c in cnf):return 0
    if var>n:return int(not cnf)
    total=0
    for value in (False,True):
        lit=var if value else -var;out=[];conflict=False
        for c in cnf:
            if lit in c:continue
            r=tuple(x for x in c if x!=-lit)
            if not r:conflict=True;break
            out.append(r)
        if not conflict:total+=count_branch(tuple(out),n,var+1)
    return total

if __name__=="__main__":
    cnf=((1,2),(-1,3))
    full=allsat(cnf,3);projected=allsat(cnf,3,[1,2])
    print("full models:",len(full),"projected models:",[k for k,_ in projected])
    assert len({k for k,_ in full})==len(full)
    brute=sum(sat(cnf,{i+1:b for i,b in enumerate(bits)}) for bits in product((False,True),repeat=3))
    assert count_branch(cnf,3)==brute==4
    expected_projection={tuple(m[v] for v in [1,2]) for _,m in full}
    assert {k for k,_ in projected}==expected_projection
    # Hands-on: decompose disconnected variable-clause components and multiply counts.

