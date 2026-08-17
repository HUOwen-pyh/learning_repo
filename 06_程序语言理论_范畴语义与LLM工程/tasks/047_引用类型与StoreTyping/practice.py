"""第 047 晚：store typing 固定每个 cell 的类型。"""
from __future__ import annotations
import sys
from dataclasses import dataclass

sys.stdout.reconfigure(encoding="utf-8")
@dataclass(frozen=True)
class BoolTy: pass
@dataclass(frozen=True)
class UnitTy: pass
@dataclass(frozen=True)
class RefTy: cell:"Ty"
Ty=BoolTy|UnitTy|RefTy; B=BoolTy(); U=UnitTy()
@dataclass(frozen=True)
class BoolV: value:bool
@dataclass(frozen=True)
class UnitV: pass
@dataclass(frozen=True)
class Loc: index:int
V=BoolV|UnitV|Loc

def value_type(v:V,sigma:tuple[Ty,...])->Ty:
    if isinstance(v,BoolV): return B
    if isinstance(v,UnitV): return U
    if not 0<=v.index<len(sigma): raise TypeError("location 不在 store typing")
    return RefTy(sigma[v.index])
def well_typed(store:tuple[V,...],sigma:tuple[Ty,...])->bool:
    return len(store)==len(sigma) and all(value_type(v,sigma)==ty for v,ty in zip(store,sigma))
def allocate(v:V,store:tuple[V,...],sigma:tuple[Ty,...]):
    ty=value_type(v,sigma); return Loc(len(store)),store+(v,),sigma+(ty,)
def typed_assign(loc:Loc,v:V,store:tuple[V,...],sigma:tuple[Ty,...]):
    if not 0<=loc.index<len(store) or len(store)!=len(sigma):
        raise IndexError("location 不在 store/store typing")
    if value_type(v,sigma)!=sigma[loc.index]: raise TypeError("赋值改变 cell 类型")
    s=list(store); s[loc.index]=v; return tuple(s)

loc,store,sigma=allocate(BoolV(True),(),())
assert loc==Loc(0) and well_typed(store,sigma)                    # 正例/空边界
assert well_typed(typed_assign(loc,BoolV(False),store,sigma),sigma)
try: typed_assign(loc,UnitV(),store,sigma)                       # 反例
except TypeError: pass
else: raise AssertionError("应拒绝异类型赋值")
for dangling in (Loc(-1),Loc(1)):
    try: typed_assign(dangling,BoolV(False),store,sigma)
    except IndexError: pass
    else: raise AssertionError("应拒绝负数或越界 location")

# 动手改造：实现 deref_type，并验证分配前旧 sigma 的所有 lookup 在扩展后保持不变。
print("047 通过：Σ 随分配扩展，赋值保持每个 cell 的稳定类型。")
