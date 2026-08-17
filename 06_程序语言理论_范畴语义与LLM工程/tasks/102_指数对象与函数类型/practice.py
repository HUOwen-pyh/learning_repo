"""有限环境上的 curry/uncurry βη 检查。"""
from __future__ import annotations
import sys
sys.stdout.reconfigure(encoding="utf-8")

def curry(f): return lambda x: lambda a: f(x, a)
def uncurry(g): return lambda x, a: g(x)(a)

def main() -> None:
    xs, aa = range(3), range(4)
    f = lambda x, a: 10 * x + a
    assert all(uncurry(curry(f))(x, a) == f(x, a) for x in xs for a in aa)
    g = lambda x: lambda a: x - a
    reg = curry(uncurry(g))
    assert all(reg(x)(a) == g(x)(a) for x in xs for a in aa)
    bad = lambda x: lambda a: a  # 丢失环境 x
    assert any(bad(x)(a) != g(x)(a) for x in xs for a in aa)
    print("curry/uncurry 的有限域 βη 检查通过")

if __name__ == "__main__": main()

# 动手改造：让环境是二元组，并证明 closure 必须保留两个分量。
