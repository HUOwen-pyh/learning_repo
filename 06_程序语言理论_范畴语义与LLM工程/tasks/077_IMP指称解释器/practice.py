"""第077晚：带 while 近似的 IMP 指称解释器。"""
from __future__ import annotations
from dataclasses import dataclass
import sys
if hasattr(sys.stdout,"reconfigure"):sys.stdout.reconfigure(encoding="utf-8")
@dataclass(frozen=True)
class N:value:int
@dataclass(frozen=True)
class V:name:str
@dataclass(frozen=True)
class Bin:op:str;a:object;b:object
@dataclass(frozen=True)
class Skip:pass
@dataclass(frozen=True)
class Assign:name:str;e:object
@dataclass(frozen=True)
class Seq:a:object;b:object
@dataclass(frozen=True)
class While:test:object;body:object
def expr(e,s):
    if isinstance(e,N):return e.value
    if isinstance(e,V):return s[e.name]
    if isinstance(e,Bin):
        a,b=expr(e.a,s),expr(e.b,s)
        return {"+":a+b,"-":a-b,"*":a*b,">":a>b}[e.op]
    raise TypeError(e)
def denote(c,s,fuel):
    if isinstance(c,Skip):return dict(s)
    if isinstance(c,Assign):
        out=dict(s);out[c.name]=expr(c.e,s);return out
    if isinstance(c,Seq):
        mid=denote(c.a,s,fuel);return None if mid is None else denote(c.b,mid,fuel)
    if isinstance(c,While):
        if not expr(c.test,s):return dict(s)
        if fuel==0:return None
        mid=denote(c.body,s,fuel);return None if mid is None else denote(c,mid,fuel-1)
    raise TypeError(c)
def main():
    body=Seq(Assign("acc",Bin("*",V("acc"),V("x"))),Assign("x",Bin("-",V("x"),N(1))))
    fact=While(Bin(">",V("x"),N(0)),body)
    assert denote(fact,{"x":4,"acc":1},4)=={"x":0,"acc":24}
    assert denote(fact,{"x":4,"acc":1},3) is None
    assert denote(fact,{"x":0,"acc":1},0)=={"x":0,"acc":1}
    diverge=While(N(1),Skip());assert denote(diverge,{},50) is None
    assert denote(Skip(),{},0)=={}                         # boundary
    print("第077晚通过：IMP 组合语义、有限近似、终止与发散样本成立。")
if __name__=="__main__":main()
# 动手改造：完成 read.md 验收项中的扩展，并为新规则补一条正例和一条反例。
