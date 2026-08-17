"""A small RUP proof checker: proof steps are independently propagated."""
def bcp_conflict(database,units):
    if any(not c for c in database):return True
    a={};queue=list(units)+[c[0] for c in database if len(c)==1]
    while queue:
        lit=queue.pop();v=abs(lit);value=lit>0
        if v in a:
            if a[v]!=value:return True
            continue
        a[v]=value
        for c in database:
            if any(a.get(abs(x))==(x>0) for x in c):continue
            unknown=[x for x in c if abs(x) not in a]
            if not unknown:return True
            if len(unknown)==1:queue.append(unknown[0])
    return False

def is_rup(database,clause):
    return bcp_conflict(database,[-l for l in clause])

def check_rup(original,proof):
    db=[tuple(c) for c in original]
    for clause in proof:
        clause=tuple(clause)
        if not is_rup(db,clause):return False
        db.append(clause)
    return bool(proof) and tuple(proof[-1])==()

if __name__=="__main__":
    formula=((1,2),(-1,2),(1,-2),(-1,-2))
    proof=((2,),(-2,),())
    for i,step in enumerate(proof):
        print("step",i,step,"RUP",is_rup(list(formula)+list(proof[:i]),step))
    assert check_rup(formula,proof)
    assert not check_rup(formula,((3,),()))
    assert not check_rup(((1,2),), ((),))
    print("valid refutation accepted; tampered proofs rejected.")
    # Hands-on: add deletion steps and ensure later hints cannot cite deleted clauses.
