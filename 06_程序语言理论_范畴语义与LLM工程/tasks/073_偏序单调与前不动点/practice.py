"""第073晚：有限偏序、单调性和前不动点。"""
from itertools import product
import sys
if hasattr(sys.stdout,"reconfigure"):sys.stdout.reconfigure(encoding="utf-8")
def powerset(xs):
    xs=list(xs);return [frozenset(x for x,b in zip(xs,bits) if b) for bits in product([0,1],repeat=len(xs))]
def leq(a,b):return a<=b
def is_poset(xs):
    refl=all(leq(x,x) for x in xs)
    anti=all(not(leq(x,y) and leq(y,x)) or x==y for x in xs for y in xs)
    trans=all(not(leq(x,y) and leq(y,z)) or leq(x,z) for x in xs for y in xs for z in xs)
    return refl and anti and trans
def monotone(f,xs):return all(not leq(x,y) or leq(f(x),f(y)) for x in xs for y in xs)
def prefixed(f,x):return leq(f(x),x)
def main():
    xs=powerset({"a","b"});assert is_poset(xs)
    f=lambda x:x|{"a"};assert monotone(f,xs)
    pres=[x for x in xs if prefixed(f,x)]
    assert frozenset({"a"}) in pres and all({"a"}<=x for x in pres)
    complement=lambda x:frozenset({"a","b"}-set(x))
    assert not monotone(complement,xs)
    assert is_poset([frozenset()])                         # singleton boundary
    print("第073晚通过：powerset 偏序、单调闭包和反例均验证。")
if __name__=="__main__":main()
# 动手改造：完成 read.md 验收项中的扩展，并为新规则补一条正例和一条反例。
