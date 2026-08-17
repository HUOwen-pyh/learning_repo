"""第083晚：Nat 观察上的有限 adequacy 实验。"""
from dataclasses import dataclass
import sys
if hasattr(sys.stdout,"reconfigure"):sys.stdout.reconfigure(encoding="utf-8")
@dataclass(frozen=True)
class Done:n:int
@dataclass(frozen=True)
class Countdown:n:int
@dataclass(frozen=True)
class Loop:pass
def operational(e,fuel):
    if isinstance(e,Done):return e.n
    if isinstance(e,Countdown):
        n=e.n
        while n>0:
            if fuel==0:return None
            fuel-=1;n-=1
        return 0
    if isinstance(e,Loop):return None
    raise TypeError(e)
def denotation(e):
    if isinstance(e,Done):return e.n
    if isinstance(e,Countdown):return 0
    if isinstance(e,Loop):return None
    raise TypeError(e)
def related(sem,obs):return sem is not None and obs==sem
def main():
    for e,fuel in [(Done(3),0),(Countdown(4),4),(Countdown(0),0)]:
        obs=operational(e,fuel);sem=denotation(e);assert related(sem,obs)
    assert denotation(Loop()) is None and operational(Loop(),100) is None
    assert operational(Countdown(4),3) is None             # insufficient evidence boundary
    assert not related(3,4)
    print("第083晚通过：Nat 逻辑关系连接终止观察与指称；预算不足单列。")
if __name__=="__main__":main()
# 动手改造：完成 read.md 验收项中的扩展，并为新规则补一条正例和一条反例。
