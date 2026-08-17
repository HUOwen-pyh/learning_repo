"""第021晚：幂集格中的直接像/逆像 Galois 连接。"""
from itertools import combinations
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

X = frozenset({0, 1, 2}); Y = frozenset({0, 1})
mapping = lambda x: x % 2

def powerset(s):
    items = tuple(sorted(s))
    return [frozenset(c) for r in range(len(items) + 1) for c in combinations(items, r)]

def image(s): return frozenset(mapping(x) for x in s)
def preimage(t): return frozenset(x for x in X if mapping(x) in t)

def check_galois(right=preimage):
    for s in powerset(X):
        for t in powerset(Y):
            if (image(s) <= t) != (s <= right(t)):
                return False, (s, t)
    return True, None

def main() -> None:
    assert (frozenset({0, 1}) & frozenset({1, 2})) == {1}   # meet
    assert (frozenset({0}) | frozenset({1})) == {0, 1}     # join
    assert check_galois() == (True, None)                   # 正例
    bad = lambda t: frozenset(x for x in X if x in t)
    ok, witness = check_galois(bad)
    assert not ok and witness is not None                   # 最小反例
    assert check_galois(lambda t: preimage(t))[0]
    print(f"通过：image ⊣ preimage；错误右伴随反例={witness}。")

if __name__ == "__main__": main()

# 动手改造：由 image∘preimage 或 preimage∘image 构造闭包，并检验单调/幂等。
