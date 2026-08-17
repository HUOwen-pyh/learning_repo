"""第078晚：环境闭包式 PCF 子集，含 fix 与 fuel。"""
from __future__ import annotations
from dataclasses import dataclass
import sys
if hasattr(sys.stdout,"reconfigure"):sys.stdout.reconfigure(encoding="utf-8")
@dataclass(frozen=True)
class N:n:int
@dataclass(frozen=True)
class Var:x:str
@dataclass(frozen=True)
class Lam:x:str;body:object
@dataclass(frozen=True)
class App:f:object;a:object
@dataclass(frozen=True)
class Pred:e:object
@dataclass(frozen=True)
class If0:c:object;z:object;s:object
@dataclass(frozen=True)
class Fix:name:str;body:object
@dataclass
class Closure:x:str;body:object;env:dict
class Timeout(Exception):pass
class EvalError(Exception):pass
def ev(e,env=None,fuel=100):
    env={} if env is None else env
    if fuel<=0:raise Timeout()
    if isinstance(e,N):return e.n
    if isinstance(e,Var):
        if e.x not in env:raise EvalError("unbound")
        v=env[e.x];return ev(v,env,fuel-1) if isinstance(v,Fix) else v
    if isinstance(e,Lam):return Closure(e.x,e.body,dict(env))
    if isinstance(e,App):
        f=ev(e.f,env,fuel-1);a=ev(e.a,env,fuel-1)
        if not isinstance(f,Closure):raise EvalError("non-function")
        return ev(f.body,{**f.env,f.x:a},fuel-1)
    if isinstance(e,Pred):return max(0,ev(e.e,env,fuel-1)-1)
    if isinstance(e,If0):
        return ev(e.z if ev(e.c,env,fuel-1)==0 else e.s,env,fuel-1)
    if isinstance(e,Fix):return ev(e.body,{**env,e.name:e},fuel-1)
    raise EvalError("unknown")
def main():
    down=Fix("f",Lam("n",If0(Var("n"),N(0),App(Var("f"),Pred(Var("n"))))))
    assert ev(App(down,N(3)),fuel=80)==0
    assert ev(App(down,N(0)),fuel=10)==0                 # base boundary
    diverge=Fix("f",Var("f"))
    try:ev(diverge,fuel=20)
    except Timeout:pass
    else:raise AssertionError("divergence produced a value")
    try:ev(App(N(1),N(2)))
    except EvalError:pass
    else:raise AssertionError("bad application accepted")
    print("第078晚通过：PCF 递归终止、基例、运行错误与发散已区分。")
if __name__=="__main__":main()
# 动手改造：完成 read.md 验收项中的扩展，并为新规则补一条正例和一条反例。
