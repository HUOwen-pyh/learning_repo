"""栈式 IR 的高度 verifier。"""
from __future__ import annotations
import sys
sys.stdout.reconfigure(encoding="utf-8")
EFFECT={"CONST":(0,1),"ADD":(2,1),"DUP":(1,2)}
def verify(code):
    height=0;heights=[]
    for pc,inst in enumerate(code):
        op=inst[0]
        if op not in EFFECT:raise ValueError(f"unknown@{pc}")
        pop,push=EFFECT[op]
        if height<pop:raise TypeError(f"underflow@{pc}")
        height=height-pop+push;heights.append(height)
    if height!=1:raise TypeError(f"final height {height}")
    return heights
def main():
    assert verify([("CONST",1),("DUP",),("ADD",)])==[1,2,1]
    for bad in [[("ADD",)],[('CONST',1),('CONST',2)],[('NOPE',)]]:
        try:verify(bad)
        except (TypeError,ValueError):pass
        else:raise AssertionError
    print("IR stack-height verifier 通过")
if __name__=="__main__":main()

# 动手改造：跟踪 Int/Bool 栈类型，拒绝 ADD 两个 Bool。
