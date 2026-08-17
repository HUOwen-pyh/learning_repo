"""Phi incoming map 的 CFG-sensitive verifier。"""
from __future__ import annotations
import sys
sys.stdout.reconfigure(encoding="utf-8")
def phi(predecessors,incoming,arrived_from):
    if set(incoming)!=set(predecessors):raise ValueError("incoming/predecessor mismatch")
    if arrived_from not in predecessors:raise ValueError("unknown edge")
    return incoming[arrived_from]
def main():
    preds={"then","else"};inc={"then":1,"else":2}
    assert phi(preds,inc,"then")==1 and phi(preds,inc,"else")==2
    for bad in [{"then":1},{"then":1,"else":2,"dead":3}]:
        try:phi(preds,bad,"then")
        except ValueError:pass
        else:raise AssertionError
    try:phi(preds,inc,"dead")
    except ValueError:pass
    else:raise AssertionError
    print("Phi predecessor-sensitive tests 通过")
if __name__=="__main__":main()

# 动手改造：为多个 Phi 同时求值，并拒绝后一个 Phi 读取同块新定义。
