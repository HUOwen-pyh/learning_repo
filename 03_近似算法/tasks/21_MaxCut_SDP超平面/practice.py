"""GW 超平面舍入内核：α_GW 一元界与 120° 三角形实验。"""
from math import acos, cos, pi
from random import Random


def ratio(theta): return 2*theta/(pi*(1-cos(theta)))


def golden_min(lo,hi,steps=100):
    for _ in range(steps):
        a=lo+(hi-lo)/3; b=hi-(hi-lo)/3
        if ratio(a)<ratio(b): hi=b
        else: lo=a
    t=(lo+hi)/2; return t,ratio(t)


def hyperplane_cut(angles,phi,edges):
    side=[cos(a-phi)>=0 for a in angles]
    return sum(w for u,v,w in edges if side[u]!=side[v])


def self_test():
    theta,alpha=golden_min(1e-5,pi)
    for k in range(1,10000):
        t=pi*k/10000
        assert t/pi+1e-12 >= alpha*(1-cos(t))/2
    angles=[0,2*pi/3,4*pi/3]; edges=[(0,1,1),(1,2,1),(0,2,1)]
    sdp=sum((1-cos(angles[u]-angles[v]))/2*w for u,v,w in edges)
    exact_expectation=sum(acos(cos(angles[u]-angles[v]))/pi*w for u,v,w in edges)
    assert abs(sdp-2.25)<1e-9 and abs(exact_expectation-2)<1e-9
    rng=Random(2121); trials=20000
    empirical=sum(hyperplane_cut(angles,rng.random()*2*pi,edges) for _ in range(trials))/trials
    print(f'alpha_GW={alpha:.6f} at theta={theta:.6f}; triangle empirical={empirical:.4f}, exact E=2')
    assert abs(empirical-exact_expectation)<.03


if __name__=='__main__': self_test()

# 动手改造：给任意二维单位向量和加权边，计算 SDP 值、解析期望与采样均值；
# 搜索最接近 α_GW 的单边夹角。
