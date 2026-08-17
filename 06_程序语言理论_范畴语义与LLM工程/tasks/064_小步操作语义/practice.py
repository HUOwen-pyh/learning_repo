"""第064晚：算术表达式的小步语义。动手改造：加入 Mul。"""
from __future__ import annotations
from dataclasses import dataclass
import sys
if hasattr(sys.stdout,"reconfigure"):sys.stdout.reconfigure(encoding="utf-8")
@dataclass(frozen=True)
class Num:value:int
@dataclass(frozen=True)
class Add:left:object;right:object
@dataclass(frozen=True)
class Bad:label:str
def value(e):return isinstance(e,Num)
def step(e):
    if isinstance(e,Add):
        if not value(e.left):
            n=step(e.left);return None if n is None else Add(n,e.right)
        if not value(e.right):
            n=step(e.right);return None if n is None else Add(e.left,n)
        return Num(e.left.value+e.right.value)
    return None
def normal(e):return step(e) is None
def run(e,limit=100):
    out=[e]
    for _ in range(limit):
        n=step(e)
        if n is None:return out
        e=n;out.append(e)
    raise RuntimeError("fuel")
def main():
    t=Add(Add(Num(1),Num(2)),Add(Num(3),Num(4)))
    assert run(t)[-1]==Num(10)
    assert value(Num(0)) and normal(Num(0))                # boundary
    stuck=Add(Num(1),Bad("x"))
    assert normal(stuck) and not value(stuck)              # negative
    assert len(run(Num(9)))==1                             # zero-step closure
    print("第064晚通过：value、normal form、stuck 与多步关系已区分。")
if __name__=="__main__":main()
# 动手改造：完成 read.md 验收项中的扩展，并为新规则补一条正例和一条反例。
