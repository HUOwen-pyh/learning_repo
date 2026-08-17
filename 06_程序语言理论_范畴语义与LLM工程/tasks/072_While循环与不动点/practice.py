"""第072晚：while functional 的有限近似。"""
from __future__ import annotations
import sys
if hasattr(sys.stdout,"reconfigure"):sys.stdout.reconfigure(encoding="utf-8")
State=dict[str,int]
Transformer=object
def bottom(state):return None
def functional(guard,body,approx):
    def run(state):
        if not guard(state):return dict(state)
        return approx(body(dict(state)))
    return run
def approximant(n,guard,body):
    w=bottom
    for _ in range(n):w=functional(guard,body,w)
    return w
def dec(s):s["x"]-=1;return s
def main():
    guard=lambda s:s["x"]>0
    assert approximant(0,guard,dec)({"x":0}) is None
    assert approximant(1,guard,dec)({"x":0})=={"x":0}
    assert approximant(2,guard,dec)({"x":1})=={"x":0}
    assert approximant(2,guard,dec)({"x":2}) is None
    assert approximant(3,guard,dec)({"x":2})=={"x":0}
    loop=lambda s:True
    assert all(approximant(n,loop,lambda s:s)({}) is None for n in range(6))
    print("第072晚通过：有限 unfolding 单调增加已定义的循环输入。")
if __name__=="__main__":main()
# 动手改造：完成 read.md 验收项中的扩展，并为新规则补一条正例和一条反例。
