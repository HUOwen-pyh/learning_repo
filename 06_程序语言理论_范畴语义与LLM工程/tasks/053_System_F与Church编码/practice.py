"""第053晚：System F 的显式类型抽象和类型应用。"""
from __future__ import annotations
from dataclasses import dataclass
import sys
if hasattr(sys.stdout, "reconfigure"): sys.stdout.reconfigure(encoding="utf-8")

@dataclass(frozen=True)
class TV: name: str
@dataclass(frozen=True)
class Base: name: str
@dataclass(frozen=True)
class Arr:
    a: object
    b: object
@dataclass(frozen=True)
class All:
    var: str
    body: object
@dataclass(frozen=True)
class Var: name: str
@dataclass(frozen=True)
class Lam:
    var: str
    ty: object
    body: object
@dataclass(frozen=True)
class App:
    f: object
    x: object
@dataclass(frozen=True)
class TLam:
    var: str
    body: object
@dataclass(frozen=True)
class TApp:
    term: object
    ty: object

class CheckError(Exception): pass

def tsubst(t: object, name: str, repl: object) -> object:
    if isinstance(t, TV): return repl if t.name == name else t
    if isinstance(t, Arr): return Arr(tsubst(t.a,name,repl),tsubst(t.b,name,repl))
    if isinstance(t, All):
        return t if t.var == name else All(t.var, tsubst(t.body,name,repl))
    return t

def synth(e: object, env: dict[str,object], tyvars: frozenset[str]=frozenset()) -> object:
    if isinstance(e, Var):
        if e.name not in env: raise CheckError("unbound")
        return env[e.name]
    if isinstance(e, Lam):
        return Arr(e.ty, synth(e.body, {**env,e.var:e.ty},tyvars))
    if isinstance(e, App):
        ft=synth(e.f,env,tyvars); xt=synth(e.x,env,tyvars)
        if not isinstance(ft,Arr) or ft.a != xt: raise CheckError("bad application")
        return ft.b
    if isinstance(e, TLam):
        return All(e.var, synth(e.body,env,tyvars|{e.var}))
    if isinstance(e, TApp):
        ft=synth(e.term,env,tyvars)
        if not isinstance(ft,All): raise CheckError("not polymorphic")
        return tsubst(ft.body,ft.var,e.ty)
    raise CheckError("unknown term")

def must_fail(f):
    try: f()
    except CheckError: return
    raise AssertionError("failure expected")

def main() -> None:
    poly_id=TLam("A",Lam("x",TV("A"),Var("x")))
    assert synth(poly_id,{}) == All("A",Arr(TV("A"),TV("A")))
    assert synth(TApp(poly_id,Base("Bool")),{}) == Arr(Base("Bool"),Base("Bool"))
    shadow=All("A",Arr(TV("A"),All("A",TV("A"))))
    assert tsubst(shadow,"A",Base("Nat")) == shadow             # binder boundary
    must_fail(lambda:synth(App(poly_id,poly_id),{}))             # term/type mismatch
    must_fail(lambda:synth(Var("z"),{}))
    print("第053晚通过：System F 的 ∀ 引入、消去和遮蔽边界成立。")

if __name__ == "__main__": main()
# 动手改造：完成 read.md 验收项中的扩展，并为新规则补一条正例和一条反例。
