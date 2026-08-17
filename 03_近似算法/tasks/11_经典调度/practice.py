"""相同并行机 List Scheduling/LPT，与 m^n 精确分配对拍。"""
from itertools import product
from random import Random


def list_schedule(jobs, m, lpt=False):
    order=sorted(range(len(jobs)),key=lambda j:-jobs[j]) if lpt else list(range(len(jobs)))
    loads=[0]*m; assignment=[[] for _ in range(m)]
    for j in order:
        i=min(range(m),key=lambda x:loads[x])
        loads[i]+=jobs[j]; assignment[i].append(j)
    return max(loads,default=0),assignment


def exact(jobs,m):
    best=sum(jobs)
    for a in product(range(m),repeat=len(jobs)):
        loads=[0]*m
        for j,i in enumerate(a): loads[i]+=jobs[j]
        best=min(best,max(loads,default=0))
    return best


def self_test():
    rng=Random(1111); worst_ls=worst_lpt=1
    for m in (2,3,4):
        for n in range(1,9):
            if m**n>70000: continue
            for _ in range(35):
                jobs=[rng.randint(1,15) for _ in range(n)]; opt=exact(jobs,m)
                ls,_=list_schedule(jobs,m); lpt,_=list_schedule(jobs,m,True)
                assert ls <= (2-1/m)*opt+1e-9
                assert lpt <= (4/3-1/(3*m))*opt+1e-9
                worst_ls=max(worst_ls,ls/opt); worst_lpt=max(worst_lpt,lpt/opt)
    print(f'observed worst: list={worst_ls:.3f}, LPT={worst_lpt:.3f}')


if __name__=='__main__': self_test()

# 动手改造：自动搜索 m=2、整数时长<=8 的最小 LPT 非最优实例，打印分配。

