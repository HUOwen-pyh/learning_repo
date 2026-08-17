"""第 040 晚：用有限实例检查 weakening/substitution schema。"""
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

def free_vars(t:T)->set[str]:
    if isinstance(t,Var): return {t.name}
    if isinstance(t,Lit): return set()
    if isinstance(t,App): return free_vars(t.fn)|free_vars(t.arg)
    return free_vars(t.body)-{t.param}
def all_names(t:T)->set[str]:
    if isinstance(t,Var): return {t.name}
    if isinstance(t,Lit): return set()
    if isinstance(t,App): return all_names(t.fn)|all_names(t.arg)
    return {t.param}|all_names(t.body)
def rename_bound(t:T,old:str,new:str)->T:
    if isinstance(t,Var): return Var(new) if t.name==old else t
    if isinstance(t,Lit): return t
    if isinstance(t,App): return App(rename_bound(t.fn,old,new),rename_bound(t.arg,old,new))
    return t if t.param==old else Abs(t.param,t.param_ty,rename_bound(t.body,old,new))

def infer(t:T,c:dict[str,Ty])->Ty:
    if isinstance(t,Var):
        if t.name not in c: raise TypeError("unbound")
        return c[t.name]
    if isinstance(t,Lit): return B
    if isinstance(t,Abs): return Arrow(t.param_ty,infer(t.body,{**c,t.param:t.param_ty}))
    f,a=infer(t.fn,c),infer(t.arg,c)
    if not isinstance(f,Arrow) or f.dom!=a: raise TypeError("bad app")
    return f.cod
def subst(t:T,x:str,s:T)->T:
    if isinstance(t,Var): return s if t.name==x else t
    if isinstance(t,App): return App(subst(t.fn,x,s),subst(t.arg,x,s))
    if isinstance(t,Abs):
        if t.param==x: return t
        if t.param in free_vars(s):
            avoid=all_names(t.body)|free_vars(s)|{x}; i=0
            while (fresh:=f"v{i}") in avoid: i+=1
            return Abs(fresh,t.param_ty,subst(rename_bound(t.body,t.param,fresh),x,s))
        return Abs(t.param,t.param_ty,subst(t.body,x,s))
    return t

identity=Abs("y",B,Var("y"))
assert infer(identity,{}) == infer(identity,{"z":B})           # weakening 正例
t=App(identity,Var("x")); assert infer(t,{"x":B})==B
assert infer(subst(t,"x",Lit(True)),{})==B                    # substitution 正例
try: infer(subst(t,"x",identity),{})                           # 反例：替入类型错
except TypeError: pass
else: raise AssertionError("应破坏 premise 而被拒绝")
shadow=Abs("x",B,Var("x")); assert subst(shadow,"x",Lit(True))==shadow  # 边界
capture_safe=subst(Abs("y",B,Var("x")),"x",Var("y"))
assert isinstance(capture_safe,Abs) and capture_safe.param!="y" and free_vars(capture_safe)=={"y"}
assert infer(capture_safe,{"y":B})==Arrow(B,B)

# 动手改造：枚举三组 Γ/A/B 实例，输出 substitution 前后类型相等证据。
print("040 通过：弱化与良类型替换的实例保持了类型。")
