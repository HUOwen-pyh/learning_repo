"""Num/Add 的 CEK 抽象机。"""
from __future__ import annotations
from dataclasses import dataclass
import sys
sys.stdout.reconfigure(encoding="utf-8")
@dataclass(frozen=True)
class Num:value:int
@dataclass(frozen=True)
class Add:a:object;b:object
@dataclass(frozen=True)
class AddL:b:object
@dataclass(frozen=True)
class AddR:a:int
def run(term):
    c=term;k=[];trace=[]
    for _ in range(100):
        trace.append((c,tuple(k)))
        if isinstance(c,Add):k.append(AddL(c.b));c=c.a
        elif isinstance(c,Num) and k:
            fr=k.pop()
            if isinstance(fr,AddL):k.append(AddR(c.value));c=fr.b
            elif isinstance(fr,AddR):c=Num(fr.a+c.value)
            else:raise TypeError(fr)
        elif isinstance(c,Num):return c.value,trace
        else:raise TypeError(c)
    raise RuntimeError("step budget")
def main():
    value,trace=run(Add(Num(1),Add(Num(2),Num(3))))
    assert value==6 and len(trace)==7 and trace[-1][1]==()
    assert run(Num(0))[0]==0
    print("CEK value=",value,"steps=",len(trace))
if __name__=="__main__":main()

# 动手改造：加入 Var/Lam/App 与 Arg/Fun frames，运行 identity application。
