"""自动寻找自然性方块的最小反例。"""
from __future__ import annotations
import itertools, sys
sys.stdout.reconfigure(encoding="utf-8")

def alpha(xs): return [x for x in xs if x != 0]
def find_counterexample():
    fs = [lambda x:x, lambda x:x+1, lambda x:0]
    for n in range(4):
        for xs in itertools.product(range(2), repeat=n):
            xs=list(xs)
            for i,f in enumerate(fs):
                left=[f(x) for x in alpha(xs)]
                right=alpha([f(x) for x in xs])
                if left != right: return xs,i,left,right
    return None

def main() -> None:
    witness=find_counterexample()
    assert witness is not None
    xs,i,left,right=witness
    assert left != right
    print(f"反例 xs={xs}, f#{i}: 左={left}, 右={right}")

if __name__ == "__main__": main()

# 动手改造：按“列表长度、函数编号”排序所有反例，并证明输出的是最小者。
