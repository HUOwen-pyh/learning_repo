"""元组张量的 associator 与 unitors。"""
from __future__ import annotations
import sys
sys.stdout.reconfigure(encoding="utf-8")

UNIT=()
def assoc_left(value):
    (a,b),c=value; return a,(b,c)
def assoc_right(value):
    a,(b,c)=value; return (a,b),c
def left_unitor(value):
    unit,a=value; assert unit==UNIT; return a
def right_unitor(value):
    a,unit=value; assert unit==UNIT; return a

def main() -> None:
    values=[((1,2),3), (("a",None),False)]
    assert all(assoc_right(assoc_left(v))==v for v in values)
    assert left_unitor((UNIT,5))==5 and right_unitor((5,UNIT))==5
    bad=lambda v:(v[0][0],(v[0][0],v[1]))
    assert bad(((1,2),3)) != assoc_left(((1,2),3))
    print("张量结合子与单位子往返通过")

if __name__ == "__main__": main()

# 动手改造：为四元嵌套值实现两条重括号路径并检查它们相等。
