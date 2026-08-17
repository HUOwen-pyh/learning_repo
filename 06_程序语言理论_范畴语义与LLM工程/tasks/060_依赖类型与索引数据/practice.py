"""第060晚：用受检 Python 对象模拟 Fin n 与 Vec A n。"""
from __future__ import annotations
from dataclasses import dataclass
import sys
if hasattr(sys.stdout,"reconfigure"):sys.stdout.reconfigure(encoding="utf-8")
@dataclass(frozen=True)
class Fin:
    value:int
    bound:int
    def __post_init__(self):
        if self.bound<=0 or not 0<=self.value<self.bound:raise ValueError("Fin witness out of range")
@dataclass(frozen=True)
class Vec:
    items:tuple
    n:int
    def __post_init__(self):
        if len(self.items)!=self.n:raise ValueError("length index mismatch")
def lookup(v:Vec,i:Fin):
    if i.bound!=v.n:raise ValueError("index belongs to another length")
    return v.items[i.value]
def append(a:Vec,b:Vec)->Vec:
    out=Vec(a.items+b.items,a.n+b.n);assert out.n==a.n+b.n;return out
def map_vec(f,v:Vec)->Vec:return Vec(tuple(map(f,v.items)),v.n)
def must_fail(f):
    try:f()
    except ValueError:return
    raise AssertionError("invalid indexed value accepted")
def main():
    v=Vec(("a","b"),2);assert lookup(v,Fin(1,2))=="b"
    assert append(Vec((),0),v)==v
    assert map_vec(str.upper,v).n==v.n
    must_fail(lambda:Fin(2,2));must_fail(lambda:Vec((1,),2));must_fail(lambda:lookup(v,Fin(0,1)))
    print("第060晚通过：Fin/Vec 模拟排除了越界和长度不一致。")
if __name__=="__main__":main()
# 动手改造：完成 read.md 验收项中的扩展，并为新规则补一条正例和一条反例。
