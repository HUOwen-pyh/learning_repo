"""第085晚：有限状态上的 partial-correctness triple。"""
from dataclasses import dataclass
import sys
if hasattr(sys.stdout,"reconfigure"):sys.stdout.reconfigure(encoding="utf-8")
@dataclass(frozen=True)
class Assign:name:str;rhs:object
def run(c,s):
    out=dict(s);out[c.name]=c.rhs(s);return out
def valid(pre,c,post,states):
    return all(not pre(s) or post(run(c,s)) for s in states)
def main():
    states=[{"x":i} for i in range(-2,3)]
    inc=Assign("x",lambda s:s["x"]+1)
    assert valid(lambda s:s["x"]>=0,inc,lambda s:s["x"]>0,states)
    assert not valid(lambda s:True,inc,lambda s:s["x"]>0,states)
    assert valid(lambda s:False,inc,lambda s:False,states) # vacuous boundary
    zero=Assign("x",lambda s:0)
    assert valid(lambda s:True,zero,lambda s:s["x"]==0,states)
    print("第085晚通过：有效、无效与空前置 Hoare triple 已区分。")
if __name__=="__main__":main()
# 动手改造：完成 read.md 验收项中的扩展，并为新规则补一条正例和一条反例。
