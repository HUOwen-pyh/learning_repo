"""第091晚：重复减法除法的 invariant、post 与 mutation test。"""
import sys
if hasattr(sys.stdout,"reconfigure"):sys.stdout.reconfigure(encoding="utf-8")
def inv(s):return s["d"]>0 and s["n"]==s["q"]*s["d"]+s["r"] and s["r"]>=0
def body(s,mutant=False):
    o=dict(s);o["r"]-=o["d"];o["q"]+=-1 if mutant else 1;return o
def verify(n,d,mutant=False):
    if d<=0:return False,None
    s={"n":n,"d":d,"q":0,"r":n}
    if not inv(s):return False,s
    while s["r"]>=s["d"]:
        s=body(s,mutant)
        if not inv(s):return False,s
    return 0<=s["r"]<d and n==s["q"]*d+s["r"],s
def main():
    for n in range(16):
        for d in range(1,7):
            ok,s=verify(n,d);assert ok and (s["q"],s["r"])==divmod(n,d)
    assert verify(0,1)[0] and verify(3,5)[1]["q"]==0       # boundaries
    assert not verify(5,0)[0]                              # excluded precondition
    ok,witness=verify(5,2,mutant=True);assert not ok and witness is not None
    print(f"第091晚通过：除法 VC 全通过；mutant 反例状态={witness}。")
if __name__=="__main__":main()
# 动手改造：完成 read.md 验收项中的扩展，并为新规则补一条正例和一条反例。
