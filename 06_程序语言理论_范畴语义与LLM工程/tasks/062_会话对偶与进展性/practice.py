"""第062晚：同步归约实验。动手改造：加入 Cancel choice。"""
from __future__ import annotations
from dataclasses import dataclass
import sys
if hasattr(sys.stdout,"reconfigure"):sys.stdout.reconfigure(encoding="utf-8")
@dataclass(frozen=True)
class End:pass
@dataclass(frozen=True)
class Send:value:object;cont:object
@dataclass(frozen=True)
class Recv:ty:type;cont:object
class Stuck(Exception):pass
def step(left,right):
    if isinstance(left,End) and isinstance(right,End):return None
    if isinstance(left,Send) and isinstance(right,Recv):
        if type(left.value) is not right.ty:raise Stuck("payload mismatch")
        return left.cont,right.cont
    if isinstance(left,Recv) and isinstance(right,Send):
        r=step(right,left);return None if r is None else (r[1],r[0])
    raise Stuck("actions are not dual")
def run(a,b,limit=20):
    n=0
    while True:
        nxt=step(a,b)
        if nxt is None:return n
        a,b=nxt;n+=1
        if n>limit:raise Stuck("step boundary")
def must_stuck(a,b):
    try:run(a,b)
    except Stuck:return
    raise AssertionError("stuck pair was accepted")
def main():
    assert run(Send("q",Recv(int,End())),Recv(str,Send(7,End())))==2
    assert run(End(),End())==0
    must_stuck(Send("a",End()),Send("b",End()))
    must_stuck(Send(1,End()),Recv(str,End()))
    must_stuck(End(),Recv(str,End()))
    print("第062晚通过：对偶双方进展，三类 stuck 配置均被识别。")
if __name__=="__main__":main()
# 动手改造：完成 read.md 验收项中的扩展，并为新规则补一条正例和一条反例。
