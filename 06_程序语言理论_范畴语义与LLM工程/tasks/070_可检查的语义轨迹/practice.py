"""第070晚：生成与独立验证带规则名的小步 trace。"""
from __future__ import annotations
from dataclasses import dataclass
import sys
if hasattr(sys.stdout,"reconfigure"):sys.stdout.reconfigure(encoding="utf-8")
@dataclass(frozen=True)
class Num:value:int
@dataclass(frozen=True)
class Add:left:object;right:object
def step(e):
    if not isinstance(e,Add):return None
    if isinstance(e.left,Add):
        p=step(e.left);return None if p is None else ("AddL",Add(p[1],e.right))
    if isinstance(e.left,Num) and isinstance(e.right,Add):
        p=step(e.right);return None if p is None else ("AddR",Add(e.left,p[1]))
    if isinstance(e.left,Num) and isinstance(e.right,Num):
        return "AddConst",Num(e.left.value+e.right.value)
    return None
def produce(e):
    trace=[(None,e)]
    while (p:=step(e)) is not None:
        rule,e=p;trace.append((rule,e))
    return trace
def verify(trace,require_normal=True):
    if not trace or trace[0][0] is not None:return False
    for i in range(1,len(trace)):
        expected=step(trace[i-1][1])
        if expected!=trace[i]:return False
    return not require_normal or step(trace[-1][1]) is None
def main():
    start=Add(Add(Num(1),Num(2)),Add(Num(3),Num(4)))
    tr=produce(start);assert verify(tr) and tr[-1][1]==Num(10)
    assert verify([(None,Num(0))])                          # zero-step boundary
    assert not verify([(None,start),(None,Num(10))])        # wrong rule / skipped steps
    assert not verify([(None,start)],require_normal=True)   # premature ending
    forged=tr.copy();forged[1]=("BAD",forged[1][1]);assert not verify(forged)
    print("第070晚通过：逐边 trace 可复核，跳步和伪造均被拒绝。")
if __name__=="__main__":main()
# 动手改造：完成 read.md 验收项中的扩展，并为新规则补一条正例和一条反例。
