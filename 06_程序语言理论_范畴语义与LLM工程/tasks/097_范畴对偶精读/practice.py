"""第097晚：有限范畴 opposite 的机械反转。"""
from dataclasses import dataclass
import sys
if hasattr(sys.stdout,"reconfigure"):sys.stdout.reconfigure(encoding="utf-8")
@dataclass(frozen=True)
class Arrow:name:str;src:str;dst:str
def opposite(arrows,comp):
    oa={name:Arrow(name,a.dst,a.src) for name,a in arrows.items()}
    oc={(f,g):h for (g,f),h in comp.items()}
    return oa,oc
def endpoints_ok(arrows,comp):
    for (g,f),h in comp.items():
        if arrows[f].dst!=arrows[g].src:return False
        if arrows[h].src!=arrows[f].src or arrows[h].dst!=arrows[g].dst:return False
    return True
def main():
    arrows={"ia":Arrow("ia","A","A"),"ib":Arrow("ib","B","B"),"f":Arrow("f","A","B")}
    comp={("ia","ia"):"ia",("ib","ib"):"ib",("f","ia"):"f",("ib","f"):"f"}
    assert endpoints_ok(arrows,comp)
    oa,oc=opposite(arrows,comp);assert endpoints_ok(oa,oc) and oa["f"]==Arrow("f","B","A")
    ooa,ooc=opposite(oa,oc);assert ooa==arrows and ooc==comp
    bad=dict(comp);bad[("ia","f")]="f";assert not endpoints_ok(arrows,bad)
    one={"i":Arrow("i","X","X")};assert opposite(one,{("i","i"):"i"})[0]==one
    print("第097晚通过：opposite 反向端点与复合顺序，双重对偶恢复原范畴。")
if __name__=="__main__":main()
# 动手改造：完成 read.md 验收项中的扩展，并为新规则补一条正例和一条反例。
