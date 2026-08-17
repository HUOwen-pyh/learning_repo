"""第058晚：类型检查后的小步规范化；fuel 不是规范化证明。"""
from __future__ import annotations
from dataclasses import dataclass
import sys
if hasattr(sys.stdout,"reconfigure"):sys.stdout.reconfigure(encoding="utf-8")
@dataclass(frozen=True)
class Base:name:str
@dataclass(frozen=True)
class Arr:a:object;b:object
@dataclass(frozen=True)
class Var:name:str
@dataclass(frozen=True)
class Lam:x:str;ty:object;body:object
@dataclass(frozen=True)
class App:f:object;x:object
class TypeFail(Exception):pass
def typ(e,env):
    if isinstance(e,Var):
        if e.name not in env:raise TypeFail("unbound")
        return env[e.name]
    if isinstance(e,Lam):return Arr(e.ty,typ(e.body,{**env,e.x:e.ty}))
    if isinstance(e,App):
        ft=typ(e.f,env);xt=typ(e.x,env)
        if not isinstance(ft,Arr) or ft.a!=xt:raise TypeFail("application")
        return ft.b
    raise TypeFail("unknown")
def subst(e,x,v):
    if isinstance(e,Var):return v if e.name==x else e
    if isinstance(e,Lam):return e if e.x==x else Lam(e.x,e.ty,subst(e.body,x,v))
    if isinstance(e,App):return App(subst(e.f,x,v),subst(e.x,x,v))
    return e
def step(e):
    if isinstance(e,App) and isinstance(e.f,Lam):return subst(e.f.body,e.f.x,e.x)
    if isinstance(e,App):
        nf=step(e.f)
        if nf is not None:return App(nf,e.x)
        nx=step(e.x)
        if nx is not None:return App(e.f,nx)
    return None
def normalize(e,fuel=100):
    typ(e,{})
    if step(e) is None:return e
    for _ in range(fuel):
        n=step(e)
        if n is None:return e
        e=n
    raise RuntimeError("fuel exhausted; this is not a theorem")
def must_fail(e):
    try:normalize(e)
    except TypeFail:return
    raise AssertionError("ill-typed term accepted")
def main():
    A=Base("A");identity=Lam("x",A,Var("x"))
    higher_identity=Lam("f",Arr(A,A),Var("f"))
    assert normalize(App(higher_identity,identity))==identity
    term=App(Lam("x",A,Var("x")),App(Lam("y",A,Var("y")),Lam("z",A,Var("z"))))
    must_fail(term)
    must_fail(Lam("x",Base("A"),App(Var("x"),Var("x"))))
    assert normalize(identity,0)==identity
    print("第058晚通过：良类型范式停止，坏 self-application 被类型系统拒绝。")
if __name__=="__main__":main()
# 动手改造：完成 read.md 验收项中的扩展，并为新规则补一条正例和一条反例。
