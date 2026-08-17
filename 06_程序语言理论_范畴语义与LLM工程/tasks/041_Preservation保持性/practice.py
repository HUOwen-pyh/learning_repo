"""第 041 晚：运行时逐步检查 preservation。"""
from __future__ import annotations
import sys
from dataclasses import dataclass

sys.stdout.reconfigure(encoding="utf-8")
@dataclass(frozen=True)
class BoolTy: pass
@dataclass(frozen=True)
class Arrow: dom:"Ty"; cod:"Ty"
Ty=BoolTy|Arrow; B=BoolTy()
@dataclass(frozen=True)
class Var: name:str
@dataclass(frozen=True)
class Lit: value:bool
@dataclass(frozen=True)
class Abs: param:str; param_ty:Ty; body:"T"
@dataclass(frozen=True)
class App: fn:"T"; arg:"T"
T=Var|Lit|Abs|App
def infer(t:T,c=None)->Ty:
    c={} if c is None else c
    if isinstance(t,Var):
        if t.name not in c: raise TypeError("unbound")
        return c[t.name]
    if isinstance(t,Lit): return B
    if isinstance(t,Abs): return Arrow(t.param_ty,infer(t.body,{**c,t.param:t.param_ty}))
    f,a=infer(t.fn,c),infer(t.arg,c)
    if not isinstance(f,Arrow) or f.dom!=a: raise TypeError("bad app")
    return f.cod
def sub(t:T,x:str,s:T)->T:
    if isinstance(t,Var): return s if t.name==x else t
    if isinstance(t,App): return App(sub(t.fn,x,s),sub(t.arg,x,s))
    if isinstance(t,Abs): return t if t.param==x else Abs(t.param,t.param_ty,sub(t.body,x,s))
    return t
def val(t:T): return isinstance(t,(Lit,Abs))
def step(t:T)->T|None:
    if not isinstance(t,App): return None
    if not val(t.fn):
        n=step(t.fn); return App(n,t.arg) if n else None
    if not val(t.arg):
        n=step(t.arg); return App(t.fn,n) if n else None
    return sub(t.fn.body,t.fn.param,t.arg) if isinstance(t.fn,Abs) else None
def checked_trace(t:T)->list[T]:
    ty=infer(t); out=[t]
    while (n:=step(t)) is not None:
        assert infer(n)==ty, "preservation violated"
        out.append(n); t=n
    return out

i=Abs("x",B,Var("x")); chain=checked_trace(App(i,App(i,Lit(True))))
assert chain[-1]==Lit(True) and all(infer(t)==B for t in chain) # 正例
try: checked_trace(App(Lit(True),Lit(False)))                   # 反例
except TypeError: pass
else: raise AssertionError("应拒绝 ill-typed 起点")
assert checked_trace(i)==[i]                                   # 边界：零步

# 动手改造：让 step 返回规则名，分别覆盖 ξ₁、ξ₂、β 三类 preservation。
print("041 通过：每个归约步骤前后均保持原类型。")

