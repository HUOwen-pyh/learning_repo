"""Maybe/List/State 的统一 Monad-law 样例。"""
from __future__ import annotations
import sys
sys.stdout.reconfigure(encoding="utf-8")

def maybe_bind(x,f): return None if x is None else f(x)
def list_bind(xs,f): return [y for x in xs for y in f(x)]
def state_pure(x): return lambda s:(x,s)
def state_bind(m,f):
    def run(s):
        x,s1=m(s); return f(x)(s1)
    return run
def state_eq(m,n): return all(m(s)==n(s) for s in range(-2,3))

def main() -> None:
    f=lambda x:None if x<0 else x+1; g=lambda x:x*2
    assert all(maybe_bind(maybe_bind(x,f),g)==maybe_bind(x,lambda a:maybe_bind(f(a),g)) for x in [None,-1,2])
    lf=lambda x:[x,x+1]; lg=lambda x:[x*2]
    assert list_bind(list_bind([1,2],lf),lg)==list_bind([1,2],lambda a:list_bind(lf(a),lg))
    tick=lambda x:lambda s:(x+s,s+1)
    m=lambda s:(2,s+1)
    assert state_eq(state_bind(state_pure(2),tick),tick(2))
    assert state_eq(state_bind(m,state_pure),m)
    print("Maybe/List/State 的代表性 Monad laws 通过")

if __name__ == "__main__": main()

# 动手改造：实现完整通用 law runner，并加入会重复执行 f 的坏 bind 反例。
