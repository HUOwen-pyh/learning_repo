"""Scanning BCP and a compact two-watched-literal propagator."""
from collections import defaultdict, deque

def scan_bcp(clauses, initial):
    assignment=dict(initial); checks=0
    while True:
        changed=False
        for clause in clauses:
            checks += 1
            if any(assignment.get(abs(l))==(l>0) for l in clause): continue
            unknown=[l for l in clause if abs(l) not in assignment]
            if not unknown: return None,checks
            if len(unknown)==1:
                lit=unknown[0]; assignment[abs(lit)]=lit>0; changed=True
        if not changed: return assignment,checks

class Watcher:
    def __init__(self,clauses):
        self.clauses=[list(c) for c in clauses]
        self.watch=defaultdict(list); self.pos=[]
        self.units=[]
        for ci,c in enumerate(self.clauses):
            if not c: self.units.append(0); self.pos.append((0,0)); continue
            j=0 if len(c)==1 else 1
            self.pos.append((0,j))
            self.watch[c[0]].append(ci)
            if j!=0:self.watch[c[j]].append(ci)
            else:self.units.append(c[0])
    @staticmethod
    def value(lit,a):
        if abs(lit) not in a:return None
        return a[abs(lit)]==(lit>0)
    def propagate(self,initial):
        a=dict(initial); q=deque(); visits=0
        def enqueue(lit):
            old=a.get(abs(lit))
            if old is not None:return old==(lit>0)
            a[abs(lit)]=lit>0;q.append(lit);return True
        for lit in self.units:
            if lit==0 or not enqueue(lit):return None,visits
        for v,val in initial.items():q.append(v if val else -v)
        while q:
            true_lit=q.popleft(); false_lit=-true_lit
            pending=self.watch[false_lit]; self.watch[false_lit]=[]
            for ci in pending:
                visits+=1;c=self.clauses[ci];i,j=self.pos[ci]
                wi,wj=c[i],c[j]
                if wi==false_lit: false_index,other_index=i,j
                elif wj==false_lit: false_index,other_index=j,i
                else: continue
                other=c[other_index]
                replacement=next((k for k,l in enumerate(c)
                                  if k not in (false_index,other_index) and self.value(l,a) is not False),None)
                if replacement is not None:
                    if false_index==i:self.pos[ci]=(replacement,j)
                    else:self.pos[ci]=(i,replacement)
                    self.watch[c[replacement]].append(ci)
                else:
                    self.watch[false_lit].append(ci)
                    ov=self.value(other,a)
                    if ov is False:return None,visits
                    if ov is None and not enqueue(other):return None,visits
        return a,visits

if __name__ == "__main__":
    cnf=((1,2),(-1,3),(-2,3),(-3,4),(4,))
    scan,checks=scan_bcp(cnf,{1:False})
    watched,visits=Watcher(cnf).propagate({1:False})
    print("closure:",watched,"scan checks:",checks,"watch visits:",visits)
    assert scan==watched and watched[2] and watched[3] and watched[4]
    conflict=((1,),(-1,))
    assert scan_bcp(conflict,{})[0] is None
    assert Watcher(conflict).propagate({})[0] is None
    # Hands-on: random CNFs and initial assignments; compare both closures/conflicts.

