"""集合、次数与顺序 trace 三种 effect grade。"""
from __future__ import annotations
from collections import Counter
import sys
sys.stdout.reconfigure(encoding="utf-8")

def grades(trace):
    return frozenset(trace),Counter(trace),tuple(trace)
def safe(trace):
    approved=False
    for e in trace:
        if e=="approve": approved=True
        if e=="call" and not approved:return False
    return True

def main() -> None:
    good=["approve","call"]; bad=["call","approve"]
    gs,gc,gt=grades(good); bs,bc,bt=grades(bad)
    assert gs==bs and gc==bc and gt!=bt
    assert safe(good) and not safe(bad)
    assert grades([])==(frozenset(),Counter(),())
    print("集合/次数丢失顺序；trace 保留策略证据")

if __name__ == "__main__": main()

# 动手改造：允许一次审批覆盖至多 k 次调用，用自动机 grade 检查。
