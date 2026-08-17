"""第087晚：三角数循环的不变量逐轮检查。"""
import sys
if hasattr(sys.stdout,"reconfigure"):sys.stdout.reconfigure(encoding="utf-8")
def run(n,invariant):
    s={"n":n,"i":0,"sum":0};trace=[dict(s)]
    if not invariant(s):return False,trace
    while s["i"]<s["n"]:
        s["i"]+=1;s["sum"]+=s["i"];trace.append(dict(s))
        if not invariant(s):return False,trace
    return True,trace
def good(s):return s["sum"]==s["i"]*(s["i"]+1)//2 and 0<=s["i"]<=s["n"]
def bad(s):return s["sum"]==s["i"]*s["i"]
def main():
    for n in range(8):
        ok,tr=run(n,good);assert ok and tr[-1]["sum"]==n*(n+1)//2
    assert run(0,good)[0]                                  # zero-iteration boundary
    ok,tr=run(3,bad);assert not ok and tr[-1]["i"]==2       # negative witness
    print("第087晚通过：三角数 invariant 初始化、保持、退出及反例均验证。")
if __name__=="__main__":main()
# 动手改造：完成 read.md 验收项中的扩展，并为新规则补一条正例和一条反例。
