"""表达式解释器、编译器与栈 VM 差分。"""
from __future__ import annotations
from dataclasses import dataclass
import random,sys
sys.stdout.reconfigure(encoding="utf-8")
@dataclass(frozen=True)
class N:v:int
@dataclass(frozen=True)
class Add:a:object;b:object
def ev(t):return t.v if isinstance(t,N) else ev(t.a)+ev(t.b)
def comp(t):return [("PUSH",t.v)] if isinstance(t,N) else comp(t.a)+comp(t.b)+[("ADD",)]
def vm(code,stack=None):
    s=list(stack or [])
    for i in code:
        if i[0]=="PUSH":s.append(i[1])
        else:b=s.pop();a=s.pop();s.append(a+b)
    return s
def gen(r,d):return N(r.randrange(10)) if d==0 else Add(gen(r,d-1),gen(r,d-1))
def main():
    r=random.Random(142)
    for _ in range(100):
        t=gen(r,3);assert vm(comp(t),[99])==[99,ev(t)]
    assert vm(comp(N(0)))==[0]
    print("100个 AST→VM differential tests 通过")
if __name__=="__main__":main()

# 动手改造：加入 Sub，故意颠倒子项编译顺序并最小化失败 AST。
