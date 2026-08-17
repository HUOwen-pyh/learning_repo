"""列表 Monad 的 eta/mu 定律。"""
from __future__ import annotations
import sys
sys.stdout.reconfigure(encoding="utf-8")

def eta(x): return [x]
def fmap(f,xs): return [f(x) for x in xs]
def mu(xss): return [x for xs in xss for x in xs]

def main() -> None:
    samples=[[],[1],[1,2]]
    for xs in samples:
        assert mu(eta(xs))==xs
        assert mu(fmap(eta,xs))==xs
    xsss=[[[1],[]],[[2,3]]]
    assert mu(mu(xsss))==mu(fmap(mu,xsss))
    bad=lambda xss:[x for xs in xss if xs for x in xs] or [None]
    assert bad([[]]) != []
    print("List Monad 的两条单位律与结合律通过")

if __name__ == "__main__": main()

# 动手改造：为 Maybe 定义 eta/mu，并让统一 law runner 同时检查两种 Monad。
