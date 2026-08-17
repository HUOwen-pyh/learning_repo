"""Gonzalez farthest-first k-center 与组合精确 oracle。"""
from itertools import combinations
from math import hypot
from random import Random


def radius(points,centers):
    return max((min(hypot(points[x][0]-points[c][0],points[x][1]-points[c][1]) for c in centers) for x in range(len(points))),default=0)


def farthest_first(points,k):
    centers=[0]; history=[]
    while len(centers)<min(k,len(points)):
        dist=[min(hypot(points[x][0]-points[c][0],points[x][1]-points[c][1]) for c in centers) for x in range(len(points))]
        history.append(max(dist)); centers.append(max(range(len(points)),key=dist.__getitem__))
    history.append(radius(points,centers))
    assert all(history[i+1]<=history[i]+1e-12 for i in range(len(history)-1))
    return centers


def exact(points,k): return min(radius(points,c) for c in combinations(range(len(points)),k))


def self_test():
    tight=[(0,0),(1,0),(2,0)]; assert radius(tight,farthest_first(tight,1))==2 and exact(tight,1)==1
    rng=Random(1818)
    for n in range(2,11):
        for k in range(1,min(4,n)+1):
            for _ in range(30):
                pts=[(rng.randrange(30),rng.randrange(30)) for _ in range(n)]
                alg=radius(pts,farthest_first(pts,k)); opt=exact(pts,k)
                assert alg<=2*opt+1e-9
    print('farthest-first <= 2*OPT; explicit ratio-2 witness checked')


if __name__=='__main__': self_test()

# 动手改造：尝试每个点作为首中心并取最好结果；证明不会破坏 2 保证，统计改善。

