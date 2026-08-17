"""第089晚：无循环命令的 weakest precondition。动手改造：加入 If。"""
from dataclasses import dataclass
import sys
if hasattr(sys.stdout,"reconfigure"):sys.stdout.reconfigure(encoding="utf-8")
@dataclass(frozen=True)
class Assign:name:str;rhs:object
@dataclass(frozen=True)
class Seq:a:object;b:object
def run(c,s):
    if isinstance(c,Assign):
        o=dict(s);o[c.name]=c.rhs(s);return o
    if isinstance(c,Seq):return run(c.b,run(c.a,s))
    raise TypeError(c)
def wp(c,post):
    if isinstance(c,Assign):return lambda s:post(run(c,s))
    if isinstance(c,Seq):return wp(c.a,wp(c.b,post))
    raise TypeError(c)
def main():
    prog=Seq(Assign("x",lambda s:s["x"]+1),Assign("y",lambda s:2*s["x"]))
    post=lambda s:s["y"]>10
    weakest=wp(prog,post)
    states=[{"x":x,"y":y} for x in range(8) for y in [0,99]]
    assert all(weakest(s)==post(run(prog,s)) for s in states)
    assert weakest({"x":5,"y":0}) and not weakest({"x":4,"y":99})
    too_wide=lambda s:s["x"]>=4
    witness=next(s for s in states if too_wide(s) and not post(run(prog,s)))
    assert witness["x"]==4
    assert wp(Assign("x",lambda s:0),lambda s:s["x"]==0)({}) # boundary
    print("第089晚通过：WP 等于语义前像，并捕获过宽前置的反例。")
if __name__=="__main__":main()
# 动手改造：完成 read.md 验收项中的扩展，并为新规则补一条正例和一条反例。
