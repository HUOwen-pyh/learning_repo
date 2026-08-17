"""第088晚：装饰倒计时循环产生三类 VC。"""
import sys
if hasattr(sys.stdout,"reconfigure"):sys.stdout.reconfigure(encoding="utf-8")
STATES=[{"n":n,"x":x} for n in range(5) for x in range(5)]
def body(s):
    o=dict(s);o["x"]-=1;return o
def vcs(pre,inv,guard,body,post,states):
    init=[s for s in states if pre(s) and not inv(s)]
    preserve=[s for s in states if inv(s) and guard(s) and not inv(body(s))]
    exit_=[s for s in states if inv(s) and not guard(s) and not post(s)]
    return {"init":init,"preserve":preserve,"exit":exit_}
def main():
    pre=lambda s:s["x"]==s["n"]
    inv=lambda s:0<=s["x"]<=s["n"]
    guard=lambda s:s["x"]>0
    post=lambda s:s["x"]==0
    good=vcs(pre,inv,guard,body,post,STATES)
    assert all(not xs for xs in good.values())
    bad_post=lambda s:s["x"]==1
    bad=vcs(pre,inv,guard,body,bad_post,STATES)
    assert bad["exit"]                                     # negative VC
    assert vcs(pre,inv,guard,body,post,[] )=={"init":[],"preserve":[],"exit":[]} # boundary
    print("第088晚通过：init/preserve/exit VC 通过，错误 post 产生反例。")
if __name__=="__main__":main()
# 动手改造：完成 read.md 验收项中的扩展，并为新规则补一条正例和一条反例。
