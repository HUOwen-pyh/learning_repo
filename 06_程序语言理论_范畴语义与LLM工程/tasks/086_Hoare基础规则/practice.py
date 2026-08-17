"""第086晚：Skip/Assign/Seq 的局部 proof certificate。"""
from dataclasses import dataclass
import sys
if hasattr(sys.stdout,"reconfigure"):sys.stdout.reconfigure(encoding="utf-8")
@dataclass(frozen=True)
class Skip:pass
@dataclass(frozen=True)
class Assign:name:str;rhs:object
@dataclass(frozen=True)
class Seq:a:object;b:object
@dataclass
class Proof:
    rule:str;pre:object;cmd:object;post:object;subs:tuple=()
def run(c,s):
    if isinstance(c,Skip):return dict(s)
    if isinstance(c,Assign):
        o=dict(s);o[c.name]=c.rhs(s);return o
    if isinstance(c,Seq):return run(c.b,run(c.a,s))
    raise TypeError(c)
def equiv(p,q,states):return all(p(s)==q(s) for s in states)
def check(p,states):
    if p.rule=="skip":return isinstance(p.cmd,Skip) and equiv(p.pre,p.post,states)
    if p.rule=="assign":
        return isinstance(p.cmd,Assign) and all(p.pre(s)==p.post(run(p.cmd,s)) for s in states)
    if p.rule=="seq":
        if not isinstance(p.cmd,Seq) or len(p.subs)!=2:return False
        a,b=p.subs
        return check(a,states) and check(b,states) and a.cmd==p.cmd.a and b.cmd==p.cmd.b and equiv(p.pre,a.pre,states) and equiv(a.post,b.pre,states) and equiv(b.post,p.post,states)
    return False
def main():
    S=[{"x":i} for i in range(4)]
    inc=Assign("x",lambda s:s["x"]+1);mid=lambda s:s["x"]==1;pre=lambda s:s["x"]==0;post=lambda s:s["x"]==2
    p1=Proof("assign",pre,inc,mid);p2=Proof("assign",mid,inc,post)
    whole=Proof("seq",pre,Seq(inc,inc),post,(p1,p2));assert check(whole,S)
    bad=Proof("assign",pre,inc,post);assert not check(bad,S)
    assert check(Proof("skip",pre,Skip(),pre),S)            # boundary
    broken=Proof("seq",pre,Seq(inc,inc),post,(p2,p1));assert not check(broken,S)
    print("第086晚通过：组合证书成立，错误赋值与断裂中间断言被拒绝。")
if __name__=="__main__":main()
# 动手改造：完成 read.md 验收项中的扩展，并为新规则补一条正例和一条反例。
