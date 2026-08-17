"""第056晚：lambda/应用/let 的紧凑 Algorithm W。"""
from __future__ import annotations
from dataclasses import dataclass
import sys
if hasattr(sys.stdout,"reconfigure"): sys.stdout.reconfigure(encoding="utf-8")

@dataclass(frozen=True)
class V: name:str
@dataclass(frozen=True)
class Fun:
    a:object
    b:object
@dataclass(frozen=True)
class Scheme:
    qs:tuple[str,...]
    body:object
@dataclass(frozen=True)
class EVar: name:str
@dataclass(frozen=True)
class Lam:
    x:str
    body:object
@dataclass(frozen=True)
class App:
    f:object
    x:object
@dataclass(frozen=True)
class Let:
    x:str
    value:object
    body:object

class InferError(Exception): pass
class Fresh:
    def __init__(self): self.n=0
    def one(self):
        v=V(f"t{self.n}"); self.n+=1; return v

def ftv(t):
    if isinstance(t,V): return {t.name}
    if isinstance(t,Fun): return ftv(t.a)|ftv(t.b)
    if isinstance(t,Scheme): return ftv(t.body)-set(t.qs)
    return set()
def apply(t,s):
    if isinstance(t,V) and t.name in s: return apply(s[t.name],s)
    if isinstance(t,Fun): return Fun(apply(t.a,s),apply(t.b,s))
    if isinstance(t,Scheme):
        return Scheme(t.qs,apply(t.body,{k:v for k,v in s.items() if k not in t.qs}))
    return t
def compose(new,old): return {k:apply(v,new) for k,v in old.items()}|new
def bind(v,t):
    if t==v:return {}
    if v.name in ftv(t):raise InferError("occurs check")
    return {v.name:t}
def unify(a,b):
    if a==b:return {}
    if isinstance(a,V):return bind(a,b)
    if isinstance(b,V):return bind(b,a)
    if isinstance(a,Fun) and isinstance(b,Fun):
        s1=unify(a.a,b.a); s2=unify(apply(a.b,s1),apply(b.b,s1)); return compose(s2,s1)
    raise InferError("cannot unify")
def apply_env(env,s): return {k:apply(v,s) for k,v in env.items()}
def inst(sc,fresh): return apply(sc.body,{q:fresh.one() for q in sc.qs})
def gen(env,t):
    ev=set()
    for sc in env.values():ev|=ftv(sc)
    return Scheme(tuple(sorted(ftv(t)-ev)),t)

def infer(e,env,fresh):
    if isinstance(e,EVar):
        if e.name not in env:raise InferError("unbound")
        return {},inst(env[e.name],fresh)
    if isinstance(e,Lam):
        a=fresh.one(); s,b=infer(e.body,{**env,e.x:Scheme((),a)},fresh)
        return s,Fun(apply(a,s),b)
    if isinstance(e,App):
        s1,tf=infer(e.f,env,fresh); s2,tx=infer(e.x,apply_env(env,s1),fresh)
        r=fresh.one(); s3=unify(apply(tf,s2),Fun(tx,r))
        return compose(s3,compose(s2,s1)),apply(r,s3)
    if isinstance(e,Let):
        s1,t1=infer(e.value,env,fresh); env1=apply_env(env,s1)
        sc=gen(env1,apply(t1,s1)); s2,t2=infer(e.body,{**env1,e.x:sc},fresh)
        return compose(s2,s1),t2
    raise InferError("unknown")

def principal(e):
    s,t=infer(e,{},Fresh()); return apply(t,s)
def must_fail(e):
    try:principal(e)
    except InferError:return
    raise AssertionError("ill-typed term accepted")

def main():
    identity=Lam("x",EVar("x"))
    assert isinstance(principal(identity),Fun)
    const=Lam("x",Lam("y",EVar("x")))
    assert isinstance(principal(const).b,Fun)
    poly=Let("id",identity,App(EVar("id"),EVar("id")))
    assert isinstance(principal(poly),Fun)
    must_fail(Lam("x",App(EVar("x"),EVar("x"))))
    must_fail(EVar("missing"))
    # Boundary: let-bound unused polymorphic identity leaves body principal.
    assert principal(Let("id",identity,Lam("z",EVar("z")))) == Fun(V("t1"),V("t1"))
    print("第056晚通过：Algorithm W 推出主类型并拒绝无限类型。")

if __name__=="__main__":main()
# 动手改造：完成 read.md 验收项中的扩展，并为新规则补一条正例和一条反例。
