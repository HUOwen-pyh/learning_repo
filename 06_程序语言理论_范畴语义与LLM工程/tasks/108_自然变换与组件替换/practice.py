"""List→Option 的自然变换及反例。"""
from __future__ import annotations
import sys
sys.stdout.reconfigure(encoding="utf-8")

def fmap_list(f,xs): return [f(x) for x in xs]
def fmap_option(f,x): return None if x is None else f(x)
def head(xs): return None if not xs else xs[0]
def bad(xs): return None if not xs or xs[0] == 0 else xs[0]

def natural(alpha, f, samples):
    return all(fmap_option(f, alpha(xs)) == alpha(fmap_list(f,xs)) for xs in samples)

def main() -> None:
    samples = [[], [0], [1], [0,2], [2,0]]
    shift = lambda x:x+1
    assert natural(head, shift, samples)
    assert not natural(bad, shift, samples)
    assert natural(head, lambda x:x*2, samples)
    print("head 自然；窥探具体值的 bad 不自然")

if __name__ == "__main__": main()

# 动手改造：检查 reverse:List→List 是否自然，并给出推导。
