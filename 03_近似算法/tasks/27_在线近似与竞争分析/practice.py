"""Ski rental：确定性 2-competitive 的穷尽验证与随机买入实验。"""
from math import e, log
from random import Random


def offline(days,B): return min(days,B)


def deterministic(days,B):
    # 前 B-1 天租；若仍继续，第 B 天买。
    return days if days<B else (B-1)+B


def randomized_from_u(days,B,u):
    # 连续时间最优分布 F(t)=(exp(t/B)-1)/(e-1), t in [0,B]。
    buy_time=B*log(1+(e-1)*u)
    return days if days<=buy_time else buy_time+B


def randomized(days,B,rng):
    return randomized_from_u(days,B,rng.random())


def self_test():
    for B in range(2,50):
        for days in range(1,5*B):
            assert deterministic(days,B)<2*offline(days,B)+1e-12
    B=40; rng=Random(2727); worst=0; trials=10000
    for days in range(1,4*B):
        # 分层分位点积分稳定核验期望；另保留一次真正随机采样供观察。
        avg=sum(randomized_from_u(days,B,(s+.5)/trials) for s in range(trials))/trials
        worst=max(worst,avg/offline(days,B))
    sampled=sum(randomized(B,B,rng) for _ in range(trials))/trials/B
    print(f'deterministic <2; stratified worst={worst:.3f}, random@B={sampled:.3f}, target={e/(e-1):.3f}')
    assert worst<1.59


if __name__=='__main__': self_test()

# 动手改造：接受预测 predicted_days；设计一个参数 λ 在一致性与鲁棒性间插值，
# 穷举真实 days/预测误差画出两条曲线。
