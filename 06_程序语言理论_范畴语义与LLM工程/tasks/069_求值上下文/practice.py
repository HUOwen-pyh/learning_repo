"""第069晚：evaluation context 的 decompose/plug。"""
from __future__ import annotations
from dataclasses import dataclass
import sys
if hasattr(sys.stdout,"reconfigure"):sys.stdout.reconfigure(encoding="utf-8")
@dataclass(frozen=True)
class Num:value:int
@dataclass(frozen=True)
class Add:left:object;right:object
@dataclass(frozen=True)
class LFrame:right:object
@dataclass(frozen=True)
class RFrame:left:Num
def plug(ctx,e):
    for f in reversed(ctx):
        e=Add(e,f.right) if isinstance(f,LFrame) else Add(f.left,e)
    return e
def decompose(e):
    ctx=[]
    while isinstance(e,Add):
        if not isinstance(e.left,Num):ctx.append(LFrame(e.right));e=e.left
        elif not isinstance(e.right,Num):ctx.append(RFrame(e.left));e=e.right
        else:return ctx,e
    return ctx,e
def contract(e):
    return Num(e.left.value+e.right.value) if isinstance(e,Add) and isinstance(e.left,Num) and isinstance(e.right,Num) else None
def step(e):
    ctx,focus=decompose(e);n=contract(focus)
    return None if n is None else plug(ctx,n)
def main():
    t=Add(Add(Num(1),Num(2)),Add(Num(3),Num(4)))
    ctx,redex=decompose(t)
    assert plug(ctx,redex)==t and redex==Add(Num(1),Num(2))
    assert step(t)==Add(Num(3),Add(Num(3),Num(4)))
    assert decompose(Num(0))==([],Num(0)) and step(Num(0)) is None
    bad=Add(Num(1),"bad");assert step(bad) is None           # stuck boundary
    print("第069晚通过：唯一分解、plug round-trip 与左到右次序成立。")
if __name__=="__main__":main()
# 动手改造：完成 read.md 验收项中的扩展，并为新规则补一条正例和一条反例。
