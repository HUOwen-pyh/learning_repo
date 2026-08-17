"""第082晚：操作解释与指称解释的有限 differential test。"""
from __future__ import annotations
from dataclasses import dataclass
import sys
if hasattr(sys.stdout,"reconfigure"):sys.stdout.reconfigure(encoding="utf-8")
@dataclass(frozen=True)
class N:n:int
@dataclass(frozen=True)
class Add:a:object;b:object
def den(e):
    return e.n if isinstance(e,N) else den(e.a)+den(e.b)
def step(e):
    if isinstance(e,N):return None
    if not isinstance(e.a,N):
        n=step(e.a);return Add(n,e.b)
    if not isinstance(e.b,N):
        n=step(e.b);return Add(e.a,n)
    return N(e.a.n+e.b.n)
def operational(e):
    while (n:=step(e)) is not None:e=n
    return e.n
def terms(depth):
    base=[N(0),N(1)]
    if depth==0:return base
    prev=terms(depth-1);return base+[Add(a,b) for a in prev for b in prev]
def bad_den(e):
    return e.n if isinstance(e,N) else bad_den(e.a)-bad_den(e.b)
def main():
    xs=terms(2);assert all(operational(e)==den(e) for e in xs)
    assert operational(N(0))==den(N(0))                  # zero-step boundary
    counter=next(e for e in xs if bad_den(e)!=operational(e))
    assert isinstance(counter,Add)
    print(f"第082晚通过：{len(xs)} 个项 sound；错误指称的反例为 {counter!r}。")
if __name__=="__main__":main()
# 动手改造：完成 read.md 验收项中的扩展，并为新规则补一条正例和一条反例。
