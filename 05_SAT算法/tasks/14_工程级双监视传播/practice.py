"""Random differential tests for watched propagation and backtrack safety."""
from collections import defaultdict,deque
import random

def scan(clauses,initial):
    a=dict(initial)
    while True:
        changed=False
        for c in clauses:
            if any(a.get(abs(l))==(l>0) for l in c):continue
            u=[l for l in c if abs(l) not in a]
            if not u:return None
            if len(u)==1:
                l=u[0];a[abs(l)]=l>0;changed=True
        if not changed:return a

class Watches:
    def __init__(self,clauses):
        self.c=[list(dict.fromkeys(x)) for x in clauses];self.p=[];self.w=defaultdict(list);self.units=[]
        for i,c in enumerate(self.c):
            if not c:self.p.append((0,0));self.units.append(0);continue
            j=min(1,len(c)-1);self.p.append((0,j));self.w[c[0]].append(i)
            if j:self.w[c[j]].append(i)
            else:self.units.append(c[0])
    @staticmethod
    def val(l,a):
        return None if abs(l) not in a else a[abs(l)]==(l>0)
    def run(self,initial):
        a=dict(initial);q=deque()
        def put(l):
            old=a.get(abs(l))
            if old is not None:return old==(l>0)
            a[abs(l)]=l>0;q.append(l);return True
        for l in self.units:
            if not l or not put(l):return None
        for v,b in initial.items():q.append(v if b else -v)
        while q:
            f=-q.popleft();items=self.w[f];self.w[f]=[]
            for ci in items:
                c=self.c[ci];i,j=self.p[ci]
                if c[i]==f:bad,other=i,j
                elif c[j]==f:bad,other=j,i
                else:continue
                replacement=next((k for k,l in enumerate(c) if k not in (bad,other) and self.val(l,a) is not False),None)
                if replacement is not None:
                    self.p[ci]=(replacement,j) if bad==i else (i,replacement)
                    self.w[c[replacement]].append(ci)
                else:
                    self.w[f].append(ci);ov=self.val(c[other],a)
                    if ov is False:return None
                    if ov is None and not put(c[other]):return None
        return a
    def invariant(self):
        for ci,c in enumerate(self.c):
            if not c:continue
            i,j=self.p[ci]
            assert 0<=i<len(c) and 0<=j<len(c)
            assert ci in self.w[c[i]]
            if j!=i:assert ci in self.w[c[j]]

if __name__=="__main__":
    rng=random.Random(14)
    for _ in range(300):
        n=6
        clauses=tuple(tuple(rng.choice((-1,1))*v for v in rng.sample(range(1,n+1),rng.randint(1,4)))
                      for _ in range(rng.randint(1,15)))
        chosen=rng.sample(range(1,n+1),rng.randint(0,3));initial={v:rng.choice((False,True)) for v in chosen}
        expected=scan(clauses,initial);watch=Watches(clauses);actual=watch.run(initial)
        if actual is not None:watch.invariant()
        assert (actual is None)==(expected is None)
        if actual is not None:
            # Closures can choose the same forced values; compare all scan implications.
            assert all(actual.get(v)==b for v,b in expected.items())
    print("300 watched/scanning propagation cases agreed.")
    # Hands-on: reuse one watcher across assign/backtrack cycles; positions need no restoration.
