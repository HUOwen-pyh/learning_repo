"""第017晚：有限群定律与逆元证书。"""
from itertools import product
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

def check_group(values, op, identity, inverse):
    for x in values:
        if op(identity, x) != x or op(x, identity) != x:
            return False, ("identity", x)
        if op(inverse(x), x) != identity or op(x, inverse(x)) != identity:
            return False, ("inverse", x)
    for a, b, c in product(values, repeat=3):
        if op(op(a, b), c) != op(a, op(b, c)):
            return False, ("associativity", a, b, c)
    return True, None

def main() -> None:
    n = 5
    add = lambda a, b: (a + b) % n
    inv = lambda a: (-a) % n
    assert check_group(range(n), add, 0, inv) == (True, None)  # 正例
    for a, b, c in product(range(n), repeat=3):
        if add(a, b) == add(a, c): assert b == c               # 消去律
    bad_inverse = lambda _: 0
    ok, why = check_group(range(n), add, 0, bad_inverse)
    assert not ok and why == ("inverse", 1)                    # 最小反例
    assert not all(any(x + y == 0 for y in range(5)) for x in range(5))
    print("通过：模5加法构成群；自然数加法并非每个元素可逆。")

if __name__ == "__main__": main()

# 动手改造：实现置换群 S3 的复合与逆，并验证它通常不交换。
