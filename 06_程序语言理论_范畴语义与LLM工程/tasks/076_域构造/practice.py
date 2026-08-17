"""第076晚：flat、product 与有限函数域的逐点序。"""
from dataclasses import dataclass
import sys
if hasattr(sys.stdout,"reconfigure"):sys.stdout.reconfigure(encoding="utf-8")
@dataclass(frozen=True)
class Bottom:pass
BOT=Bottom()
def flat_leq(a,b):return a==BOT or a==b
def prod_leq(a,b):return flat_leq(a[0],b[0]) and flat_leq(a[1],b[1])
POINTS=(0,1,2)
def fun_leq(f,g):return all(flat_leq(f[x],g[x]) for x in POINTS)
def monotone_chain_map(f):
    return all(i>j or flat_leq(f[i],f[j]) for i in POINTS for j in POINTS)
def main():
    assert flat_leq(BOT,"v") and flat_leq("v","v")
    assert not flat_leq("v","w") and not flat_leq("v",BOT)
    assert prod_leq((BOT,"x"),("a","x"))
    assert not prod_leq(("a","x"),("a","y"))
    f={0:BOT,1:"x",2:"x"};g={0:"x",1:"x",2:"x"}
    assert fun_leq(f,g) and monotone_chain_map(f)
    bad={0:"x",1:BOT,2:"x"};assert not monotone_chain_map(bad)
    assert prod_leq((BOT,BOT),(BOT,BOT))                   # boundary
    print("第076晚通过：三种域构造的 pointwise 信息序已验证。")
if __name__=="__main__":main()
# 动手改造：完成 read.md 验收项中的扩展，并为新规则补一条正例和一条反例。
