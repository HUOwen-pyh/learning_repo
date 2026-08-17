"""Conservative learned-clause reduction with locked reasons."""
from dataclasses import dataclass

@dataclass
class Clause:
    literals: tuple[int,...]
    lbd: int
    activity: float
    learned: bool=True
    deleted: bool=False

def reduce_database(original,learned,locked,target_fraction=.5):
    assert all(not c.learned for c in original)
    candidates=[c for c in learned if id(c) not in locked and c.lbd>2]
    # Worse: high LBD, low activity, long size.
    candidates.sort(key=lambda c:(c.lbd,-c.activity,len(c.literals)),reverse=True)
    count=int(len(learned)*target_fraction)
    for c in candidates[:count]:c.deleted=True
    return original+[c for c in learned if not c.deleted]

if __name__=="__main__":
    original=[Clause((1,2),2,0,learned=False)]
    learned=[Clause((-1,3),2,1.0),Clause((2,4,5),3,.2),
             Clause((-2,6,7,8),4,.1),Clause((3,-5),3,4.0)]
    locked={id(learned[2])}
    active=reduce_database(original,learned,locked)
    print("kept:",[(c.literals,c.lbd,c.activity) for c in active])
    assert original[0] in active
    assert learned[0] in active  # glue
    assert learned[2] in active  # locked
    assert all(not c.deleted for c in active)
    assert any(c.deleted for c in learned)
    reasons={7:learned[2]}
    assert all(reason in active for reason in reasons.values())
    # Hands-on: mark-delete first, then rebuild watches and remap clause IDs.

