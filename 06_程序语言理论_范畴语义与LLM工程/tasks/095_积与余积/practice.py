"""第095晚：FinSet 中 product/coproduct 的中介箭头。"""
from itertools import product
import sys
if hasattr(sys.stdout,"reconfigure"):sys.stdout.reconfigure(encoding="utf-8")
def pairing(X,f,g):return {x:(f[x],g[x]) for x in X}
def copair(A,B,f,g):
    return {("L",a):f[a] for a in A}|{("R",b):g[b] for b in B}
def all_maps(X,Y):
    X=list(X)
    for vals in product(tuple(Y),repeat=len(X)):yield dict(zip(X,vals))
def main():
    X={0,1};A={"a","b"};B={False,True}
    f={0:"a",1:"b"};g={0:True,1:False};u=pairing(X,f,g)
    assert all(u[x][0]==f[x] and u[x][1]==g[x] for x in X)
    candidates=[h for h in all_maps(X,set(product(A,B))) if all(h[x][0]==f[x] and h[x][1]==g[x] for x in X)]
    assert candidates==[u]
    co=copair(A,B,{"a":0,"b":1},{False:2,True:3})
    assert co[("L","b")]==1 and co[("R",True)]==3
    assert pairing(set(),{}, {})=={}                      # empty-source boundary
    wrong={0:("a",False),1:("b",False)};assert wrong not in candidates
    print("第095晚通过：积/余积交换方程与 mediator 唯一性成立。")
if __name__=="__main__":main()
# 动手改造：完成 read.md 验收项中的扩展，并为新规则补一条正例和一条反例。
