"""第 039 晚：可执行 progress：done 或 step。"""
from __future__ import annotations
import sys
from dataclasses import dataclass

sys.stdout.reconfigure(encoding="utf-8")
@dataclass(frozen=True)
class BoolTy: pass
@dataclass(frozen=True)
class Arrow: dom: "Ty"; cod: "Ty"
Ty = BoolTy | Arrow; B=BoolTy()
@dataclass(frozen=True)
class Var: name: str
@dataclass(frozen=True)
class Lit: value: bool
@dataclass(frozen=True)
class Abs: param: str; param_ty: Ty; body: "T"
@dataclass(frozen=True)
class App: fn: "T"; arg: "T"
T=Var|Lit|Abs|App

def infer(t:T, c:dict[str,Ty]|None=None)->Ty:
    c={} if c is None else c
    if isinstance(t,Var):
        if t.name not in c: raise TypeError("free variable")
        return c[t.name]
    if isinstance(t,Lit): return B
    if isinstance(t,Abs): return Arrow(t.param_ty,infer(t.body,{**c,t.param:t.param_ty}))
    f,a=infer(t.fn,c),infer(t.arg,c)
    if not isinstance(f,Arrow) or f.dom!=a: raise TypeError("bad application")
    return f.cod
def sub(t:T,x:str,s:T)->T:
    if isinstance(t,Var): return s if t.name==x else t
    if isinstance(t,App): return App(sub(t.fn,x,s),sub(t.arg,x,s))
    if isinstance(t,Abs): return t if t.param==x else Abs(t.param,t.param_ty,sub(t.body,x,s))
    return t
def value(t:T)->bool: return isinstance(t,(Lit,Abs))
def step(t:T)->T|None:
    if not isinstance(t,App): return None
    if not value(t.fn):
        n=step(t.fn); return App(n,t.arg) if n else None
    if not value(t.arg):
        n=step(t.arg); return App(t.fn,n) if n else None
    return sub(t.fn.body,t.fn.param,t.arg) if isinstance(t.fn,Abs) else None
def progress(t:T)->tuple[str,T]:
    infer(t,{})
    if value(t): return ("done",t)
    nxt=step(t)
    if nxt is None: raise AssertionError("typed closed term stuck")
    return ("step",nxt)

i=Abs("x",B,Var("x"))
assert progress(App(i,Lit(True))) == ("step",Lit(True))         # 正例
try: progress(App(Lit(True),Lit(False)))                        # 反例
except TypeError: pass
else: raise AssertionError("ill-typed 项不在定理域内")
assert progress(i)==("done",i)                                # 边界

# 动手改造：加入 If，扩展 progress 的测试矩阵并保持无 stuck 分支。
print("039 通过：闭且良类型的项必为值或能走一步。")

