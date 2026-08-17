"""第065晚：Bool/Nat 静态语义与 progress 小实验。"""
from __future__ import annotations
from dataclasses import dataclass
import sys
if hasattr(sys.stdout,"reconfigure"):sys.stdout.reconfigure(encoding="utf-8")
@dataclass(frozen=True)
class Lit:value:bool|int
@dataclass(frozen=True)
class Succ:e:object
@dataclass(frozen=True)
class If:c:object;t:object;f:object
class TypeFail(Exception):pass
def typ(e):
    if isinstance(e,Lit):return "Bool" if isinstance(e.value,bool) else "Nat"
    if isinstance(e,Succ):
        if typ(e.e)!="Nat":raise TypeFail("succ")
        return "Nat"
    if isinstance(e,If):
        if typ(e.c)!="Bool":raise TypeFail("condition")
        a,b=typ(e.t),typ(e.f)
        if a!=b:raise TypeFail("branches")
        return a
    raise TypeFail("unknown")
def value(e):return isinstance(e,Lit)
def step(e):
    if isinstance(e,Succ):
        if isinstance(e.e,Lit) and type(e.e.value) is int:return Lit(e.e.value+1)
        n=step(e.e);return None if n is None else Succ(n)
    if isinstance(e,If):
        if e.c==Lit(True):return e.t
        if e.c==Lit(False):return e.f
        n=step(e.c);return None if n is None else If(n,e.t,e.f)
    return None
def must_fail(e):
    try:typ(e)
    except TypeFail:return
    raise AssertionError("ill-typed accepted")
def main():
    good=If(Lit(True),Lit(0),Succ(Lit(0)))
    assert typ(good)=="Nat" and step(good)==Lit(0)
    for e in [Lit(True),Lit(0),Succ(Lit(0)),good]:
        typ(e);assert value(e) or step(e) is not None
    must_fail(If(Lit(0),Lit(True),Lit(False)))
    must_fail(If(Lit(True),Lit(0),Lit(False)))
    assert typ(Succ(Lit(0)))=="Nat"
    print("第065晚通过：静态规则排除错误，闭良类型样本满足 progress。")
if __name__=="__main__":main()
# 动手改造：完成 read.md 验收项中的扩展，并为新规则补一条正例和一条反例。
