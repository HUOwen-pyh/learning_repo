"""第081晚：STLC 子集的环境式组合指称与替换。"""
from __future__ import annotations
from dataclasses import dataclass
import sys
if hasattr(sys.stdout,"reconfigure"):sys.stdout.reconfigure(encoding="utf-8")
@dataclass(frozen=True)
class N:n:int
@dataclass(frozen=True)
class Var:x:str
@dataclass(frozen=True)
class Add:a:object;b:object
@dataclass(frozen=True)
class Lam:x:str;body:object
@dataclass(frozen=True)
class App:f:object;a:object
def den(e,env):
    if isinstance(e,N):return e.n
    if isinstance(e,Var):return env[e.x]
    if isinstance(e,Add):return den(e.a,env)+den(e.b,env)
    if isinstance(e,Lam):return lambda v:den(e.body,{**env,e.x:v})
    if isinstance(e,App):return den(e.f,env)(den(e.a,env))
    raise TypeError(e)
def subst(e,x,v):
    if isinstance(e,Var):return v if e.x==x else e
    if isinstance(e,N):return e
    if isinstance(e,Add):return Add(subst(e.a,x,v),subst(e.b,x,v))
    if isinstance(e,App):return App(subst(e.f,x,v),subst(e.a,x,v))
    if isinstance(e,Lam):return e if e.x==x else Lam(e.x,subst(e.body,x,v))
    raise TypeError(e)
def main():
    inc=Lam("x",Add(Var("x"),N(1)))
    assert den(App(inc,N(4)),{})==5                       # beta
    e=Add(Var("x"),N(2));v=N(3)
    assert den(subst(e,"x",v),{})==den(e,{"x":den(v,{})})
    shadow=Lam("x",Var("x"));assert subst(shadow,"x",N(9))==shadow
    assert den(N(0),{"unused":9})==0                     # environment boundary
    print("第081晚通过：组合指称、beta 与代表性替换引理实例成立。")
if __name__=="__main__":main()
# 动手改造：完成 read.md 验收项中的扩展，并为新规则补一条正例和一条反例。
