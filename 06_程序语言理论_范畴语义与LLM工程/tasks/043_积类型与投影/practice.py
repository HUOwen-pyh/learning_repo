"""第 043 晚：积类型与投影。"""
from __future__ import annotations
import sys
from dataclasses import dataclass

sys.stdout.reconfigure(encoding="utf-8")
@dataclass(frozen=True)
class BoolTy: pass
@dataclass(frozen=True)
class Prod: left:"Ty"; right:"Ty"
Ty=BoolTy|Prod; B=BoolTy()
@dataclass(frozen=True)
class Lit: value:bool
@dataclass(frozen=True)
class Pair: left:"T"; right:"T"
@dataclass(frozen=True)
class Fst: pair:"T"
@dataclass(frozen=True)
class Snd: pair:"T"
T=Lit|Pair|Fst|Snd

def infer(t:T)->Ty:
    if isinstance(t,Lit): return B
    if isinstance(t,Pair): return Prod(infer(t.left),infer(t.right))
    p=infer(t.pair)
    if not isinstance(p,Prod): raise TypeError("只能投影积")
    return p.left if isinstance(t,Fst) else p.right
def value(t:T)->bool:
    return isinstance(t,Lit) or isinstance(t,Pair) and value(t.left) and value(t.right)
def step(t:T)->T|None:
    if isinstance(t,Pair):
        if not value(t.left):
            left=step(t.left); return Pair(left,t.right) if left is not None else None
        if not value(t.right):
            right=step(t.right); return Pair(t.left,right) if right is not None else None
        return None
    if isinstance(t,(Fst,Snd)):
        if not value(t.pair):
            pair=step(t.pair); return type(t)(pair) if pair is not None else None
        if isinstance(t.pair,Pair) and value(t.pair):
            return t.pair.left if isinstance(t,Fst) else t.pair.right
    return None

p=Pair(Lit(True),Lit(False))
assert infer(p)==Prod(B,B) and step(Fst(p))==Lit(True)          # 正例
try: infer(Fst(Lit(True)))                                     # 反例
except TypeError: pass
else: raise AssertionError("应拒绝非积投影")
assert step(Snd(p))==Lit(False) and value(Pair(Lit(True),Lit(False)))  # 边界
ordered=Pair(Fst(p),Snd(p))
assert step(ordered)==Pair(Lit(True),Snd(p))                    # 必须先归约左字段
assert step(Fst(Pair(Fst(p),Lit(False))))==Fst(Pair(Lit(True),Lit(False)))

# 动手改造：让 pair 子项可归约，按 ST_Pair1/ST_Pair2 实现左到右顺序。
print("043 通过：积的构造、类型和两个投影已对齐。")
