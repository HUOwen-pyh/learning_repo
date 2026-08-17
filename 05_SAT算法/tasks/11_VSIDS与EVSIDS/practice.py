"""A deterministic EVSIDS activity model with rescaling."""
import heapq

class EVSIDS:
    def __init__(self,n,decay=.95,rescale_at=1e4):
        self.activity={v:0.0 for v in range(1,n+1)}
        self.increment=1.0;self.decay=decay;self.rescale_at=rescale_at
    def bump_conflict(self,variables):
        for v in variables:self.activity[v]+=self.increment
        self.increment/=self.decay
        if max(self.activity.values(),default=0)>self.rescale_at:
            factor=1/self.rescale_at
            self.activity={v:s*factor for v,s in self.activity.items()}
            self.increment*=factor
    def ranking(self,assigned=frozenset()):
        return sorted((v for v in self.activity if v not in assigned),
                      key=lambda v:(-self.activity[v],v))
    def pick(self,assigned=frozenset()):
        order=self.ranking(assigned);return order[0] if order else None

if __name__=="__main__":
    h=EVSIDS(5,rescale_at=20)
    for conflict in [{1,2},{1,3},{1,2},{4},{1,4},{4},{4}]:
        before=h.ranking();h.bump_conflict(conflict);after=h.ranking()
        print(conflict,"->",after,[round(h.activity[v],2) for v in after])
    assert h.pick({4})!=4
    before=h.ranking();h.activity={v:s*0.01 for v,s in h.activity.items()}
    assert h.ranking()==before
    assert h.pick()==4
    # Hands-on: maintain a lazy heap and discard stale/assigned entries.

