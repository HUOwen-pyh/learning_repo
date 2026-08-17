"""有限集合模型中的恒等与复合。"""
from __future__ import annotations
import sys
sys.stdout.reconfigure(encoding="utf-8")

def identity(x: int) -> int:
    return x

def compose(g, f):
    return lambda x: g(f(x))

def ext_equal(f, g, domain: set[int]) -> bool:
    return all(f(x) == g(x) for x in domain)

def main() -> None:
    a = {0, 1, 2}
    f = lambda x: (x + 1) % 3
    g = lambda x: 2 - x
    h = lambda x: x * x
    assert ext_equal(compose(identity, f), f, a)
    assert ext_equal(compose(f, identity), f, a)
    assert ext_equal(compose(h, compose(g, f)), compose(compose(h, g), f), a)
    bad_identity = lambda x: 0
    assert not ext_equal(compose(bad_identity, f), f, a)
    print("有限模型：恒等律、结合律和最小反例均通过")

if __name__ == "__main__":
    main()

# 动手改造：加入第二个三元素函数模型，检查一个翻译是否同时保存恒等与复合。
