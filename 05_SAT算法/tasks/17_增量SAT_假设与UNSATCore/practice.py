"""A tiny incremental SAT session with temporary assumptions and core shrinking."""
from itertools import product

def verify(cnf,m):return all(any(m[abs(l)]==(l>0) for l in c) for c in cnf)

def solve(cnf,assumptions=()):
    n=max([abs(l) for c in cnf for l in c]+[abs(l) for l in assumptions]+[0])
    fixed={abs(l):l>0 for l in assumptions}
    if len(fixed)<len({abs(l) for l in assumptions}):return None
    if any(l in assumptions and -l in assumptions for l in assumptions):return None
    free=[v for v in range(1,n+1) if v not in fixed]
    return next((fixed|dict(zip(free,bits)) for bits in product((False,True),repeat=len(free))
                 if verify(cnf,fixed|dict(zip(free,bits)))),None)

class Session:
    def __init__(self):self.cnf=[]
    def add(self,clause):self.cnf.append(tuple(clause))
    def solve(self,assumptions=()):return solve(tuple(self.cnf),tuple(assumptions))
    def core(self,assumptions):
        assert self.solve(assumptions) is None
        core=list(dict.fromkeys(assumptions));i=0
        while i<len(core):
            trial=core[:i]+core[i+1:]
            if self.solve(trial) is None:core=trial
            else:i+=1
        return tuple(core)

if __name__=="__main__":
    s=Session();s.add((1,2));s.add((-1,3));s.add((-2,3))
    assert s.solve((3,)) is not None
    assumptions=(-3,4,-4,2)
    assert s.solve(assumptions) is None
    core=s.core(assumptions)
    print("assumptions:",assumptions,"subset-minimal core:",core)
    assert set(core)<=set(assumptions) and s.solve(core) is None
    assert all(s.solve(core[:i]+core[i+1:]) is not None for i in range(len(core)))
    assert s.solve((1,)) is not None  # no assumption leakage
    # Hands-on: distinguish duplicate and contradictory assumptions in the API.

