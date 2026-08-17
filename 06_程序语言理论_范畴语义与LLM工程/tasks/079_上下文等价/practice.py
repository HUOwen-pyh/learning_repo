"""第079晚：有限上下文族中的可区分性实验。"""
from dataclasses import dataclass
import sys
if hasattr(sys.stdout,"reconfigure"):sys.stdout.reconfigure(encoding="utf-8")
@dataclass(frozen=True)
class Hole:pass
@dataclass(frozen=True)
class N:n:int
@dataclass(frozen=True)
class Add:a:object;b:object
@dataclass(frozen=True)
class IsZero:e:object
def fill(c,e):
    if isinstance(c,Hole):return e
    if isinstance(c,Add):return Add(fill(c.a,e),fill(c.b,e))
    if isinstance(c,IsZero):return IsZero(fill(c.e,e))
    return c
def ev(e):
    if isinstance(e,N):return e.n
    if isinstance(e,Add):return ev(e.a)+ev(e.b)
    if isinstance(e,IsZero):return ev(e.e)==0
    raise TypeError(e)
def witness(a,b,contexts):
    for c in contexts:
        if ev(fill(c,a))!=ev(fill(c,b)):return c
    return None
def main():
    contexts=[Hole(),Add(Hole(),N(0)),Add(Hole(),N(1)),IsZero(Hole())]
    assert witness(N(0),N(1),contexts) is not None
    assert witness(Add(N(0),N(2)),N(2),contexts) is None
    assert witness(N(0),N(0),[]) is None                  # empty-test boundary
    assert ev(fill(Add(Hole(),N(1)),N(2)))==3
    print("第079晚通过：有界上下文找到区分 witness，并保留“非完整判定”边界。")
if __name__=="__main__":main()
# 动手改造：完成 read.md 验收项中的扩展，并为新规则补一条正例和一条反例。
