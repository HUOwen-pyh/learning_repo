"""第016晚：有限幺半群检查和分块聚合。"""
from itertools import product
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

def check_monoid(values, op, identity):
    for x in values:
        if op(identity, x) != x or op(x, identity) != x:
            return False, ("identity", x)
    for a, b, c in product(values, repeat=3):
        if op(op(a, b), c) != op(a, op(b, c)):
            return False, ("associativity", a, b, c)
    return True, None

def fold_monoid(xs, op, identity):
    result = identity
    for x in xs: result = op(result, x)
    return result

def main() -> None:
    ok, _ = check_monoid(range(5), lambda a, b: (a + b) % 5, 0)
    assert ok                                                     # 最小正例
    assert fold_monoid([], lambda a, b: a + b, 0) == 0           # 空边界
    xs = [1, 2, 3, 4]
    whole = fold_monoid(xs, lambda a, b: a + b, 0)
    chunks = fold_monoid([sum(xs[:2]), sum(xs[2:])], lambda a, b: a + b, 0)
    assert whole == chunks
    ok, why = check_monoid(range(5), lambda a, b: (a + b) % 5, 1)
    assert not ok and why[0] == "identity"                        # 最小反例
    print("通过：单位元处理空批次，结合律保证分块结果一致。")

if __name__ == "__main__": main()

# 动手改造：用 (sum,count) 幺半群实现可并行合并的平均数。
