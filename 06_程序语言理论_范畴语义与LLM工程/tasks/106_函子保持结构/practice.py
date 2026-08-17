"""小型幺半群范畴上的函子定律检查。"""
from __future__ import annotations
import sys
sys.stdout.reconfigure(encoding="utf-8")

def is_monoid_functor(mapping: dict[int,int], source_mod: int, target_mod: int) -> bool:
    elems = range(source_mod)
    if mapping.get(0) != 0: return False
    return all(mapping[(a+b)%source_mod] == (mapping[a]+mapping[b])%target_mod
               for a in elems for b in elems)

def main() -> None:
    good = {0:0, 1:2, 2:1}
    bad_identity = {0:1, 1:0, 2:2}
    assert is_monoid_functor(good, 3, 3)
    assert not is_monoid_functor(bad_identity, 3, 3)
    assert is_monoid_functor({0:0}, 1, 5)
    print("函子定律：恒等与复合均保持")

if __name__ == "__main__": main()

# 动手改造：穷举 Z3→Z3 的所有映射，列出恰有多少个幺半群函子。
