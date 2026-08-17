"""Set Cover 重复随机舍入 + singleton alteration，比较理论漏盖界。"""
from math import ceil, exp, log
from random import Random


def round_and_repair(n,sets,x,R,rng):
    picked=set()
    for _ in range(R):
        for i,q in enumerate(x):
            if rng.random()<q: picked.add(i)
    covered=set().union(*(sets[i] for i in picked)) if picked else set()
    missed=set(range(n))-covered
    # 前 n 个集合约定为 singleton。
    picked.update(missed)
    return picked,len(missed)


def self_test():
    rng=Random(1414); n,d=40,5
    sets=[{e} for e in range(n)]
    # d 个平移窗口；每元素恰落在 d 个窗口中。
    windows=[{(start+k)%n for k in range(d)} for start in range(n)]
    sets+=windows; x=[0.0]*n+[1/d]*n
    assert all(abs(sum(x[i] for i,s in enumerate(sets) if e in s)-1)<1e-9 for e in range(n))
    R=ceil(log(n)+2); trials=4000; misses=0; any_miss=0
    for _ in range(trials):
        picked,missed=round_and_repair(n,sets,x,R,rng)
        union=set().union(*(sets[i] for i in picked))
        assert len(union)==n
        misses+=missed; any_miss+=missed>0
    bound=n*exp(-R)
    print(f'R={R}, empirical P(any miss)={any_miss/trials:.4f}, union bound={bound:.4f}')
    assert any_miss/trials <= min(1.0,4*bound)  # 固定种子的宽松统计体检


if __name__=='__main__': self_test()

# 动手改造：记录修复前成本、修复成本和未覆盖数；用同一个 U~Uniform(0,1)
# 决定全部集合的错误相关版，观察乘积界为何不再匹配。

