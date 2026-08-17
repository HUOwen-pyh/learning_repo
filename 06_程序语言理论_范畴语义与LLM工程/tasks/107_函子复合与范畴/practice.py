"""Option 与 List 映射的函子复合。"""
from __future__ import annotations
import sys
sys.stdout.reconfigure(encoding="utf-8")

def option_map(f, x): return None if x is None else f(x)
def list_map(f, xs): return [f(x) for x in xs]
def nested_map(f, xs): return list_map(lambda x: option_map(f, x), xs)

def main() -> None:
    xs = [1, None, 3]
    ident = lambda x:x
    f, g = lambda x:x+2, lambda x:x*3
    assert nested_map(ident, xs) == xs
    assert nested_map(lambda x:g(f(x)), xs) == nested_map(g, nested_map(f, xs))
    wrong = nested_map(lambda x:f(g(x)), xs)
    assert wrong != nested_map(lambda x:g(f(x)), xs)
    assert nested_map(f, []) == []
    print("List∘Option 的函子复合定律通过")

if __name__ == "__main__": main()

# 动手改造：再加入 Result(E, A)，比较三层函子的两种括号方式。
