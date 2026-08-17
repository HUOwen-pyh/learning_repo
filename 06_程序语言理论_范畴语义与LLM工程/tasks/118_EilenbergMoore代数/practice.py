"""List Monad 的 Eilenberg–Moore algebra laws。"""
from __future__ import annotations
import math, sys
sys.stdout.reconfigure(encoding="utf-8")

def check(algebra, unit_value, samples, nested):
    unit=all(algebra([x])==x for x in samples)
    assoc=all(algebra([algebra(xs) for xs in xss])==algebra([x for xs in xss for x in xs]) for xss in nested)
    return unit and assoc and algebra([])==unit_value

def main() -> None:
    nested=[[[1],[2,3]], [[],[4]], [[1,2],[3,4]]]
    assert check(sum,0,[1,2,3],nested)
    product=lambda xs:math.prod(xs)
    assert check(product,1,[1,2,3],nested)
    mean=lambda xs:sum(xs)/len(xs) if xs else 0
    assert not check(mean,0,[1,2,3],nested)
    print("sum/product 是 List algebra；mean 的分组会改变结果")

if __name__ == "__main__": main()

# 动手改造：打印 mean 违反结合律的最小嵌套列表。
