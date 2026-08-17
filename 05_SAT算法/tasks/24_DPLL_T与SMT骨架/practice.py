"""Lazy SAT modulo equality/disequality with theory lemmas."""
from itertools import product

class DSU:
    def __init__(self,n):self.p=list(range(n))
    def find(self,x):
        while x!=self.p[x]:self.p[x]=self.p[self.p[x]];x=self.p[x]
        return x
    def union(self,a,b):
        a,b=self.find(a),self.find(b)
        if a!=b:self.p[b]=a

def theory_conflict(atoms,boolean_model,nterms):
    d=DSU(nterms);positive=[]
    for v,(a,b) in atoms.items():
        if boolean_model[v]:d.union(a,b);positive.append(v)
    for v,(a,b) in atoms.items():
        if not boolean_model[v] and d.find(a)==d.find(b):
            # Negate the conjunction of all selected equalities and this disequality.
            return tuple([-p for p in positive]+[v])
    return None

def sat_cnf(cnf,nvars):
    for bits in product((False,True),repeat=nvars):
        m={i+1:b for i,b in enumerate(bits)}
        if all(any(m[abs(l)]==(l>0) for l in c) for c in cnf):yield m

def lazy_smt(cnf,atoms,nterms):
    db=list(cnf);lemmas=[]
    while True:
        model=next(sat_cnf(db,len(atoms)),None)
        if model is None:return None,lemmas
        lemma=theory_conflict(atoms,model,nterms)
        if lemma is None:return model,lemmas
        db.append(lemma);lemmas.append(lemma)

if __name__=="__main__":
    # v1:a=b, v2:b=c, v3:a=c. Require v1,v2,not v3: Boolean SAT, theory UNSAT.
    atoms={1:(0,1),2:(1,2),3:(0,2)}
    model,lemmas=lazy_smt(((1,),(2,),(-3,)),atoms,3)
    print("model:",model,"theory lemmas:",lemmas)
    assert model is None and lemmas
    # Lemma (-1 or -2 or 3) is equality-theory valid.
    assert (-1 in lemmas[0] and -2 in lemmas[0] and 3 in lemmas[0])
    model2,_=lazy_smt(((1,),(-2,),(-3,)),atoms,3)
    assert model2 is not None and theory_conflict(atoms,model2,3) is None
    # Hands-on: minimize the equality path used in a theory explanation.

