"""第057晚：命题即类型、证明即项。动手改造：加入 Sum/case。"""
from __future__ import annotations
from dataclasses import dataclass
import sys
if hasattr(sys.stdout,"reconfigure"):sys.stdout.reconfigure(encoding="utf-8")
@dataclass(frozen=True)
class Atom:name:str
@dataclass(frozen=True)
class Imp:a:object;b:object
@dataclass(frozen=True)
class And:a:object;b:object
@dataclass(frozen=True)
class Var:name:str
@dataclass(frozen=True)
class Lam:x:str;assumption:object;body:object
@dataclass(frozen=True)
class App:f:object;x:object
@dataclass(frozen=True)
class Pair:left:object;right:object
@dataclass(frozen=True)
class Fst:p:object
@dataclass(frozen=True)
class Snd:p:object
class ProofError(Exception):pass
def infer(t,ctx):
    if isinstance(t,Var):
        if t.name not in ctx:raise ProofError("unbound assumption")
        return ctx[t.name]
    if isinstance(t,Lam):return Imp(t.assumption,infer(t.body,{**ctx,t.x:t.assumption}))
    if isinstance(t,App):
        f=infer(t.f,ctx);x=infer(t.x,ctx)
        if not isinstance(f,Imp) or f.a!=x:raise ProofError("invalid modus ponens")
        return f.b
    if isinstance(t,Pair):return And(infer(t.left,ctx),infer(t.right,ctx))
    if isinstance(t,(Fst,Snd)):
        p=infer(t.p,ctx)
        if not isinstance(p,And):raise ProofError("projection from non-conjunction")
        return p.a if isinstance(t,Fst) else p.b
    raise ProofError("unknown proof")
def must_fail(f):
    try:f()
    except ProofError:return
    raise AssertionError("invalid proof accepted")
def main():
    A,B,C=Atom("A"),Atom("B"),Atom("C")
    compose=Lam("ab",Imp(A,B),Lam("bc",Imp(B,C),Lam("a",A,App(Var("bc"),App(Var("ab"),Var("a"))))))
    assert infer(compose,{})==Imp(Imp(A,B),Imp(Imp(B,C),Imp(A,C)))
    swap=Lam("p",And(A,B),Pair(Snd(Var("p")),Fst(Var("p"))))
    assert infer(swap,{})==Imp(And(A,B),And(B,A))
    must_fail(lambda:infer(App(Lam("x",A,Var("x")),Lam("y",B,Var("y"))),{}))
    must_fail(lambda:infer(Var("missing"),{}))
    assert infer(Pair(Var("a"),Var("b")),{"a":A,"b":B})==And(A,B)
    print("第057晚通过：proof term 精确对应自然演绎。")
if __name__=="__main__":main()
# 动手改造：完成 read.md 验收项中的扩展，并为新规则补一条正例和一条反例。
