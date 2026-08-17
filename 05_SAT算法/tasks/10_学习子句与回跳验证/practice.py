"""Independent checks for entailment, LBD, and asserting clauses."""
from itertools import product

def sat_clause(clause,model):
    return any(model[abs(l)]==(l>0) for l in clause)

def entails(cnf,clause,n):
    return all(not all(sat_clause(c,m) for c in cnf) or sat_clause(clause,m)
               for bits in product((False,True),repeat=n)
               for m in ({i+1:b for i,b in enumerate(bits)},))

def lbd(clause,levels):
    return len({levels[abs(l)] for l in clause})

def status(clause,assignment):
    if any(assignment.get(abs(l))==(l>0) for l in clause):return "satisfied"
    unknown=[l for l in clause if abs(l) not in assignment]
    return "conflict" if not unknown else ("unit" if len(unknown)==1 else "open")

if __name__=="__main__":
    cnf=((-2,3),(-1,-3,4),(-3,-4))
    learned=(-1,-3)
    levels={1:1,2:2,3:2,4:2}
    assert entails(cnf,learned,4)
    assert lbd(learned,levels)==2
    after_backjump={1:True}
    print("learned:",learned,"LBD:",lbd(learned,levels),
          "status after jump:",status(learned,after_backjump))
    assert status(learned,after_backjump)=="unit"
    tampered=(-1,3)
    assert not entails(cnf,tampered,4)
    # A learned clause with two unassigned literals is not asserting.
    assert status((-1,-3,4),after_backjump)=="open"
    # Hands-on: return a countermodel when entailment fails.

