"""第 046 晚：显式 store 的引用机器。"""
from __future__ import annotations
import sys
from dataclasses import dataclass

sys.stdout.reconfigure(encoding="utf-8")
@dataclass(frozen=True)
class BoolV: value:bool
@dataclass(frozen=True)
class UnitV: pass
@dataclass(frozen=True)
class Loc: index:int
Value=BoolV|UnitV|Loc
Store=tuple[Value,...]

def allocate(v:Value, store:Store)->tuple[Loc,Store]:
    return Loc(len(store)), store+(v,)
def deref(loc:Loc, store:Store)->Value:
    if not 0<=loc.index<len(store): raise IndexError("悬空 location")
    return store[loc.index]
def assign(loc:Loc,v:Value,store:Store)->tuple[UnitV,Store]:
    if not 0<=loc.index<len(store): raise IndexError("悬空 location")
    cells=list(store); cells[loc.index]=v
    return UnitV(),tuple(cells)

loc,s1=allocate(BoolV(True),())
assert loc==Loc(0) and s1==(BoolV(True),)                    # 正例/首地址边界
assert deref(loc,s1)==BoolV(True) and s1==(BoolV(True),)    # read 不变
unit,s2=assign(loc,BoolV(False),s1); assert unit==UnitV() and deref(loc,s2)==BoolV(False)
try: deref(Loc(1),s1)                                      # 反例
except IndexError: pass
else: raise AssertionError("应拒绝越界 location")

# 动手改造：定义 Config(term,store) 与 step，逐条对应三条 SF reduction rule。
print("046 通过：分配、读取、写入都显式转移 store 配置。")

