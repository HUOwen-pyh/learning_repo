"""第 042 晚：组合 progress/preservation 的安全 STLC runner。"""
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
@dataclass(frozen=True)
class If: guard:"T"; yes:"T"; no:"T"
T=Var|Lit|Abs|App|If
def infer(t:T,c=None)->Ty:
    c={} if c is None else c
    if isinstance(t,Var):
        if t.name not in c: raise TypeError("unbound")
        return c[t.name]
    if isinstance(t,Lit): return B
    if isinstance(t,Abs): return Arrow(t.param_ty,infer(t.body,{**c,t.param:t.param_ty}))
    if isinstance(t,App):
        f,a=infer(t.fn,c),infer(t.arg,c)
        if not isinstance(f,Arrow) or f.dom!=a: raise TypeError("bad app")
        return f.cod
    if infer(t.guard,c)!=B: raise TypeError("bad guard")
    y,n=infer(t.yes,c),infer(t.no,c)
    if y!=n: raise TypeError("branch mismatch")
    return y
def sub(t:T,x:str,s:T)->T:
    if isinstance(t,Var): return s if t.name==x else t
    if isinstance(t,App): return App(sub(t.fn,x,s),sub(t.arg,x,s))
    if isinstance(t,If): return If(sub(t.guard,x,s),sub(t.yes,x,s),sub(t.no,x,s))
    if isinstance(t,Abs): return t if t.param==x else Abs(t.param,t.param_ty,sub(t.body,x,s))
    return t
def val(t:T): return isinstance(t,(Lit,Abs))
def step(t:T)->T|None:
    if isinstance(t,If):
        if isinstance(t.guard,Lit): return t.yes if t.guard.value else t.no
        g=step(t.guard); return If(g,t.yes,t.no) if g else None
    if isinstance(t,App):
        if not val(t.fn):
            f=step(t.fn); return App(f,t.arg) if f else None
        if not val(t.arg):
            a=step(t.arg); return App(t.fn,a) if a else None
        return sub(t.fn.body,t.fn.param,t.arg) if isinstance(t.fn,Abs) else None
    return None
@dataclass(frozen=True)
class Result: status:str; term:T; ty:Ty; steps:int
def safe_run(t:T,gas:int=30)->Result:
    if gas < 0: raise ValueError("gas 必须非负")
    ty=infer(t)
    if val(t): return Result("done",t,ty,0)
    for used in range(gas):
        n=step(t)
        if n is None: raise AssertionError("progress violated: typed term stuck")
        assert infer(n)==ty
        t=n
        if val(t): return Result("done",t,ty,used+1)
    return Result("out-of-gas",t,ty,gas)  # 不计算并丢弃预算外的一步。

i=Abs("x",B,Var("x")); assert safe_run(App(i,Lit(True))).term==Lit(True)
try: safe_run(App(Lit(True),Lit(False)))                        # 反例
except TypeError: pass
else: raise AssertionError("应在执行前拒绝")
assert safe_run(Lit(False),0)==Result("done",Lit(False),B,0)   # 边界

# 动手改造：生成一批深度受限闭项，汇总 done/rejected/out-of-gas 与规则覆盖率。
print("042 通过：验证、progress、preservation 与预算已组合为安全 runner。")
