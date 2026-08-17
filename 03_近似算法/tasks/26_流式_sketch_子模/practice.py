"""Count-Min Sketch + 正确 OPT 猜测下的流式 coverage 1/2 内核。"""
from itertools import combinations
from math import ceil, e, log
from random import Random


class CountMin:
    P=2_147_483_647
    def __init__(self,epsilon,delta,seed=0):
        self.w=ceil(e/epsilon); self.d=ceil(log(1/delta)); rng=Random(seed)
        self.ab=[(rng.randrange(1,self.P),rng.randrange(self.P)) for _ in range(self.d)]
        self.table=[[0]*self.w for _ in range(self.d)]
    def _h(self,x,a,b): return ((a*x+b)%self.P)%self.w
    def add(self,x,count=1):
        for row,(a,b) in enumerate(self.ab): self.table[row][self._h(x,a,b)]+=count
    def query(self,x): return min(self.table[r][self._h(x,*self.ab[r])] for r in range(self.d))


def stream_threshold(sets,k,opt,order):
    chosen=[]; covered=set(); threshold=opt/(2*k)
    for i in order:
        gain=len(sets[i]-covered)
        if len(chosen)<k and gain+1e-12>=threshold:
            chosen.append(i); covered|=sets[i]
    return chosen,len(covered)


def self_test():
    rng=Random(2626); cms=CountMin(.08,.01,26); exact={}
    for _ in range(6000):
        x=rng.randrange(400); cms.add(x); exact[x]=exact.get(x,0)+1
    assert all(cms.query(x)>=c for x,c in exact.items())
    print('Count-Min max observed overestimate:',max(cms.query(x)-c for x,c in exact.items()))
    for n in range(4,11):
        for _ in range(80):
            sets=[{x for x in range(n) if rng.random()<.35} for __ in range(n)]
            k=rng.randint(1,min(4,n)); opt=max(len(set().union(*(sets[i] for i in c))) for c in combinations(range(n),k))
            order=list(range(n)); rng.shuffle(order)
            chosen,val=stream_threshold(sets,k,opt,order)
            assert len(chosen)<=k and val*2>=opt
    print('correct-guess streaming threshold always reached OPT/2')


if __name__=='__main__': self_test()

# 动手改造：并行维护 v=(1+eps)^i 的多个 threshold 解，只保留
# max_singleton <= v <= 2k*max_singleton，最终返回价值最大者。

