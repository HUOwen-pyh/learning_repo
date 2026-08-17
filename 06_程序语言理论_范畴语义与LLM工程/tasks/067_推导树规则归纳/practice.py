"""第067晚：可局部检查的 big-step derivation tree。"""
from __future__ import annotations
from dataclasses import dataclass
import sys
if hasattr(sys.stdout,"reconfigure"):sys.stdout.reconfigure(encoding="utf-8")
@dataclass(frozen=True)
class Num:value:int
@dataclass(frozen=True)
class Add:left:object;right:object
@dataclass(frozen=True)
class Deriv:
    rule:str
    expr:object
    value:int
    premises:tuple["Deriv",...]=()
def derive(e):
    if isinstance(e,Num):return Deriv("E_Num",e,e.value)
    if isinstance(e,Add):
        a,b=derive(e.left),derive(e.right)
        return Deriv("E_Add",e,a.value+b.value,(a,b))
    raise TypeError(e)
def check(d):
    if d.rule=="E_Num":
        return isinstance(d.expr,Num) and d.value==d.expr.value and d.premises==()
    if d.rule=="E_Add":
        if not isinstance(d.expr,Add) or len(d.premises)!=2:return False
        a,b=d.premises
        return check(a) and check(b) and a.expr==d.expr.left and b.expr==d.expr.right and d.value==a.value+b.value
    return False
def main():
    d=derive(Add(Num(2),Add(Num(3),Num(4))))
    assert check(d) and d.value==9
    assert check(derive(Num(0)))                           # boundary
    forged=Deriv("E_Add",Add(Num(1),Num(2)),99,(derive(Num(1)),derive(Num(2))))
    assert not check(forged)
    assert not check(Deriv("E_Num",Num(1),1,(derive(Num(1)),)))
    print("第067晚通过：合法推导可复核，伪造结论和前提均被拒绝。")
if __name__=="__main__":main()
# 动手改造：完成 read.md 验收项中的扩展，并为新规则补一条正例和一条反例。
