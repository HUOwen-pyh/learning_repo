"""CONST/ADD 的 SECD 子集。"""
from __future__ import annotations
import sys
sys.stdout.reconfigure(encoding="utf-8")

def run(code):
    s=[];e={};c=list(code);d=[];trace=[]
    while c:
        trace.append((tuple(s),dict(e),tuple(c),tuple(d)))
        op,*args=c.pop(0)
        if op=="CONST":s.append(args[0])
        elif op=="ADD":
            if len(s)<2:raise RuntimeError("underflow")
            b=s.pop();a=s.pop();s.append(a+b)
        else:raise ValueError(op)
    if len(s)!=1:raise RuntimeError("bad final stack")
    return s[0],trace
def main():
    v,t=run([("CONST",1),("CONST",2),("CONST",3),("ADD",),("ADD",)])
    assert v==6 and len(t)==5
    for bad in [[("ADD",)],[('CONST',1),('CONST',2)]]:
        try:run(bad)
        except RuntimeError:pass
        else:raise AssertionError
    print("SECD子集 value=6 steps=5")
if __name__=="__main__":main()

# 动手改造：加入 LD/ST 环境指令，并给未绑定变量失败位置。
