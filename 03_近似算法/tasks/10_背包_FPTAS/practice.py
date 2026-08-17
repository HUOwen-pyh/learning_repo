"""0/1 Knapsack 利润缩放 FPTAS；返回集合并用穷举验证。"""
from fractions import Fraction
from random import Random


def fptas(items, capacity, epsilon):
    keep=[(i,w,p) for i,(w,p) in enumerate(items) if w<=capacity and p>0]
    if not keep: return []
    n=len(keep); pmax=max(p for _,_,p in keep)
    eps=Fraction(str(epsilon)); scale=[(p*n*eps.denominator)//(eps.numerator*pmax) for _,_,p in keep]
    total=sum(scale); inf=10**18
    dp=[inf]*(total+1); take=[None]*(total+1); dp[0]=0
    for pos,(_,w,_) in enumerate(keep):
        q=scale[pos]
        for val in range(total-q,-1,-1):
            if dp[val]<inf and dp[val]+w<dp[val+q]:
                dp[val+q]=dp[val]+w; take[val+q]=(val,pos)
    val=max(v for v in range(total+1) if dp[v]<=capacity)
    ans=[]
    while val:
        prev,pos=take[val]; ans.append(keep[pos][0]); val=prev
    return ans


def exact(items, capacity):
    best=0
    for mask in range(1<<len(items)):
        w=sum(items[i][0] for i in range(len(items)) if mask>>i&1)
        if w<=capacity: best=max(best,sum(items[i][1] for i in range(len(items)) if mask>>i&1))
    return best


def self_test():
    rng=Random(1010)
    for n in range(1,14):
        for _ in range(35):
            items=[(rng.randint(1,25),rng.randint(1,40)) for _ in range(n)]
            cap=rng.randint(1,60); opt=exact(items,cap)
            for eps in (.5,.25,.1):
                chosen=fptas(items,cap,eps)
                assert sum(items[i][0] for i in chosen)<=cap
                val=sum(items[i][1] for i in chosen)
                assert val+1e-9 >= (1-eps)*opt
    print('FPTAS feasibility and (1-epsilon) guarantee verified')


if __name__=='__main__': self_test()

# 动手改造：让函数同时返回 DP 状态数；对 epsilon=0.5,...,0.02 输出
# (状态数, value/OPT)，并检查精度提高时理论下界如何变化。
