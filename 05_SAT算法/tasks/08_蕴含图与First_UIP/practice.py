"""Resolution along a hand-built implication graph to first UIP."""
from itertools import product

def resolve(a,b,var):
    assert var in a and -var in b or -var in a and var in b
    out=(set(a)|set(b))-({var,-var})
    assert not any(-l in out for l in out)
    return frozenset(out)

def entails(cnf,clause,n):
    for bits in product((False,True),repeat=n):
        m={i+1:b for i,b in enumerate(bits)}
        if all(any(m[abs(l)]==(l>0) for l in c) for c in cnf):
            if not any(m[abs(l)]==(l>0) for l in clause):return False
    return True

if __name__=="__main__":
    # Decisions: x1@1, x2@2. Reasons imply x3,x4; (-x3 or -x4) conflicts.
    r3=frozenset((-2,3))
    r4=frozenset((-1,-3,4))
    conflict=frozenset((-3,-4))
    cnf=(r3,r4,conflict)
    levels={1:1,2:2,3:2,4:2};trail=[1,2,3,4]
    learned=conflict
    chain=[]
    while sum(levels[abs(l)]==2 for l in learned)>1:
        pivot=next(abs(l) for assigned in reversed(trail) for l in learned
                   if abs(l)==abs(assigned) and abs(l) in (3,4))
        reason={3:r3,4:r4}[pivot]
        old=learned;learned=resolve(learned,reason,pivot);chain.append((old,reason,pivot,learned))
    backjump=max((levels[abs(l)] for l in learned if levels[abs(l)]<2),default=0)
    print("resolution chain:",chain)
    print("first-UIP learned:",sorted(learned),"backjump:",backjump)
    assert learned==frozenset((-1,-3)) and backjump==1
    assert entails(cnf,learned,4)
    assert sum(levels[abs(l)]==2 for l in learned)==1
    # Hands-on: change trail order and show why reverse-trail pivot selection matters.

