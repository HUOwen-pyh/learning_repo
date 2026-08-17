"""第096晚：有限 Set 的 exponential、eval、curry/uncurry。"""
from itertools import product
import sys
if hasattr(sys.stdout,"reconfigure"):sys.stdout.reconfigure(encoding="utf-8")
def functions(A,B):
    A=tuple(A);return [dict(zip(A,vals)) for vals in product(tuple(B),repeat=len(A))]
def curry(h,C,A):
    return {c:{a:h[(c,a)] for a in A} for c in C}
def uncurry(k,C,A):
    return {(c,a):k[c][a] for c in C for a in A}
def main():
    A=(0,1);B=("x","y");C=(False,True)
    exp=functions(A,B);assert len(exp)==len(B)**len(A)==4
    h={(c,a):B[(int(c)+a)%2] for c in C for a in A}
    k=curry(h,C,A);assert uncurry(k,C,A)==h               # beta
    assert curry(uncurry(k,C,A),C,A)==k                  # eta
    for c in C:
        for a in A:assert k[c][a]==h[(c,a)]              # evaluation
    assert functions((),B)==[{}]                         # B^0 singleton
    print("第096晚通过：exponential 基数、eval 与 curry/uncurry βη 律成立。")
if __name__=="__main__":main()
# 动手改造：完成 read.md 验收项中的扩展，并为新规则补一条正例和一条反例。
