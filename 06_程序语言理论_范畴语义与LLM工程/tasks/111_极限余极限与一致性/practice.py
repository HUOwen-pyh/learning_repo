"""有限集合映射的 pullback。"""
from __future__ import annotations
from itertools import product
import sys
sys.stdout.reconfigure(encoding="utf-8")

def pullback(xs,ys,f,g):
    return [(x,y) for x in xs for y in ys if f(x)==g(y)]

def enumerate_mediators(zs,pb,u,v):
    """枚举所有 Z→PB 函数，并只保留两个投影分别等于 u、v 的候选。"""
    candidates=[]
    for outputs in product(pb, repeat=len(zs)):
        mediator=dict(zip(zs,outputs))
        if all(mediator[z][0]==u[z] and mediator[z][1]==v[z] for z in zs):
            candidates.append(mediator)
    return candidates

def main() -> None:
    xs,ys=range(4),"abcde"
    f=lambda x:x%2
    g=lambda y:ord(y)%2
    pb=pullback(xs,ys,f,g)
    assert pb
    assert all(f(x)==g(y) for x,y in pb)
    # 任何兼容锥都有且仅有一个同时保持两个投影的 mediator。
    zs=[10,11]
    u={10:0,11:1}; v={10:"b",11:"a"}
    expected={z:(u[z],v[z]) for z in zs}
    mediators=enumerate_mediators(zs,pb,u,v)
    assert mediators == [expected]                              # 存在且唯一

    # 明确构造第二候选：只改一个输出；它至少破坏一条投影方程，故被排除。
    second=dict(expected)
    second[10]=next(pair for pair in pb if pair != expected[10])
    assert second not in mediators
    assert any(second[z][0]!=u[z] or second[z][1]!=v[z] for z in zs)
    print("pullback 大小:",len(pb),"；唯一 mediator:",mediators[0])

if __name__ == "__main__": main()

# 动手改造：实现 equalizer(f,g)，并把它写成 pullback 的特例。
