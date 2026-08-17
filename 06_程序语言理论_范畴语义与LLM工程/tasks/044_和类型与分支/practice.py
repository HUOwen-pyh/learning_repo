"""第 044 晚：带类型注解的 sum 与 exhaustive case。"""
from __future__ import annotations
import sys
from dataclasses import dataclass

sys.stdout.reconfigure(encoding="utf-8")
@dataclass(frozen=True)
class BoolTy: pass
@dataclass(frozen=True)
class Sum: left:"Ty"; right:"Ty"
Ty=BoolTy|Sum; B=BoolTy()
@dataclass(frozen=True)
class Var: name:str
@dataclass(frozen=True)
class Lit: value:bool
@dataclass(frozen=True)
class Inl: value:"T"; right_ty:Ty
@dataclass(frozen=True)
class Inr: left_ty:Ty; value:"T"
@dataclass(frozen=True)
class Case: scrut:"T"; lx:str; left:"T"; rx:str; right:"T"
T=Var|Lit|Inl|Inr|Case
def infer(t:T,c=None)->Ty:
    c={} if c is None else c
    if isinstance(t,Var):
        if t.name not in c: raise TypeError("unbound")
        return c[t.name]
    if isinstance(t,Lit): return B
    if isinstance(t,Inl): return Sum(infer(t.value,c),t.right_ty)
    if isinstance(t,Inr): return Sum(t.left_ty,infer(t.value,c))
    s=infer(t.scrut,c)
    if not isinstance(s,Sum): raise TypeError("case 需要和类型")
    l=infer(t.left,{**c,t.lx:s.left}); r=infer(t.right,{**c,t.rx:s.right})
    if l!=r: raise TypeError("case 分支结果类型不同")
    return l
def sub(t:T,x:str,v:T)->T:
    if isinstance(t,Var): return v if t.name==x else t
    if isinstance(t,Lit): return t
    if isinstance(t,Inl): return Inl(sub(t.value,x,v),t.right_ty)
    if isinstance(t,Inr): return Inr(t.left_ty,sub(t.value,x,v))
    left=t.left if t.lx==x else sub(t.left,x,v)
    right=t.right if t.rx==x else sub(t.right,x,v)
    return Case(sub(t.scrut,x,v),t.lx,left,t.rx,right)
def value(t:T)->bool:
    return isinstance(t,Lit) or isinstance(t,Inl) and value(t.value) or isinstance(t,Inr) and value(t.value)
def step(t:T)->T|None:
    if not isinstance(t,Case): return None
    if not value(t.scrut):
        scrut=step(t.scrut); return Case(scrut,t.lx,t.left,t.rx,t.right) if scrut is not None else None
    if isinstance(t.scrut,Inl): return sub(t.left,t.lx,t.scrut.value)
    if isinstance(t.scrut,Inr): return sub(t.right,t.rx,t.scrut.value)
    return None

good=Case(Inl(Lit(True),B),"x",Var("x"),"e",Lit(False))
assert infer(good)==B and step(good)==Lit(True)                 # 正例
bad=Case(Inl(Lit(True),B),"x",Var("x"),"e",Inl(Lit(False),B))
try: infer(bad)                                                 # 反例
except TypeError: pass
else: raise AssertionError("应拒绝分支错型")
right=Case(Inr(B,Lit(False)),"x",Lit(True),"y",Var("y"))
assert step(right)==Lit(False)                                 # 边界：inr
compound=Case(Inl(Lit(True),B),"x",Inl(Var("x"),B),"e",Inr(B,Var("e")))
assert step(compound)==Inl(Lit(True),B)                        # payload 替换必须穿过分支 AST

# 动手改造：使 scrutinee 可小步归约，并添加 ST_Case congruence 分支。
print("044 通过：和类型的 tag、case 与分支类型已对齐。")
