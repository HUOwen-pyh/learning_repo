"""Shmoys–Tardos 分槽舍入内核：纯标准库二分图增广路。"""
from math import ceil
from random import Random


def slot_round(p,x):
    m,n=len(p),len(p[0]); slots=[]; adj=[set() for _ in range(n)]
    for i in range(m):
        jobs=sorted((j for j in range(n) if x[i][j]>1e-12),key=lambda j:-p[i][j])
        mass=sum(x[i]); count=ceil(mass-1e-12)
        local=[len(slots)+k for k in range(count)]; slots += [(i,k) for k in range(count)]
        pos=0.0
        for j in jobs:
            left=x[i][j]
            while left>1e-12:
                k=min(int(pos+1e-10),count-1); room=(k+1)-pos; take=min(left,room)
                if take>1e-12: adj[j].add(local[k])
                pos+=take; left-=take
    owner={}
    def augment(j,seen):
        for s in adj[j]:
            if s in seen: continue
            seen.add(s)
            if s not in owner or augment(owner[s],seen): owner[s]=j; return True
        return False
    for j in range(n): assert augment(j,set()), 'fractional matching should satisfy Hall'
    assignment=[None]*n
    for s,j in owner.items(): assignment[j]=slots[s][0]
    assert all(i is not None for i in assignment)
    return assignment


def self_test():
    rng=Random(1212)
    for m in range(2,6):
        for n in range(2,12):
            for _ in range(30):
                p=[[rng.randint(1,30) for _ in range(n)] for _ in range(m)]
                x=[[0.0]*n for _ in range(m)]
                for j in range(n):
                    a,b=rng.sample(range(m),2); q=rng.random()
                    x[a][j]=q; x[b][j]=1-q
                frac=[sum(p[i][j]*x[i][j] for j in range(n)) for i in range(m)]
                support_max=max(p[i][j] for i in range(m) for j in range(n) if x[i][j]>1e-12)
                T=max(max(frac),support_max)
                a=slot_round(p,x); loads=[0]*m
                for j,i in enumerate(a): loads[i]+=p[i][j]
                assert max(loads)<=2*T+1e-8
    print('slot rounding produced integral assignments with makespan <= 2T')


if __name__=='__main__': self_test()

# 动手改造：返回每个 slot 的分片列表，逐机打印“分数负载、最大支持作业、
# 舍入负载”；然后去掉降序，随机搜索界被破坏的见证。

