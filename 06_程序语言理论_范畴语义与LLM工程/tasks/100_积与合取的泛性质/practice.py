"""有限集合中积的存在唯一性。"""
from __future__ import annotations
import itertools, sys
sys.stdout.reconfigure(encoding="utf-8")

def all_maps(domain, codomain):
    for values in itertools.product(codomain, repeat=len(domain)):
        yield dict(zip(domain, values))

def mediators(x, a, b, f, g):
    product = [(u, v) for u in a for v in b]
    return [h for h in all_maps(x, product)
            if all(h[z][0] == f[z] and h[z][1] == g[z] for z in x)]

def main() -> None:
    x, a, b = [0, 1], ["L", "R"], [False, True]
    f, g = {0: "L", 1: "R"}, {0: True, 1: False}
    hs = mediators(x, a, b, f, g)
    assert len(hs) == 1
    assert hs[0] == {0: ("L", True), 1: ("R", False)}
    bad = {z: (f[z], False) for z in x}
    assert any(bad[z][1] != g[z] for z in x)
    print("积的唯一中介映射:", hs[0])

if __name__ == "__main__":
    main()

# 动手改造：把 X 改成三元素集合，并统计总映射数与满足投影方程的映射数。
