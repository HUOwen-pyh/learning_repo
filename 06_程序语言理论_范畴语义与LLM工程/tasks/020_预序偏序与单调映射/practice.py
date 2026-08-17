"""第020晚：有限预序/偏序与单调映射检查。"""
from itertools import product
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

def check_poset(values, leq):
    for x in values:
        if not leq(x, x): return False, ("reflexive", x)
    for x, y in product(values, repeat=2):
        if leq(x, y) and leq(y, x) and x != y:
            return False, ("antisymmetric", x, y)
    for x, y, z in product(values, repeat=3):
        if leq(x, y) and leq(y, z) and not leq(x, z):
            return False, ("transitive", x, y, z)
    return True, None

def monotone(values, leq1, leq2, fn):
    return all(not leq1(x, y) or leq2(fn(x), fn(y))
               for x, y in product(values, repeat=2))

def main() -> None:
    values = (1, 2, 3, 6)
    divides = lambda a, b: b % a == 0
    assert check_poset(values, divides) == (True, None)        # 正例
    assert monotone(values, divides, lambda a, b: a <= b, lambda x: x)
    ok, why = check_poset(values, lambda a, b: a < b)
    assert not ok and why[0] == "reflexive"                   # 最小反例
    strings = ("a", "b", "aa")
    ok, why = check_poset(strings, lambda a, b: len(a) <= len(b))
    assert not ok and why[0] == "antisymmetric"               # 预序非偏序
    print("通过：整除是偏序；长度关系只给预序；严格序不自反。")

if __name__ == "__main__": main()

# 动手改造：计算整除偏序的 cover 关系并输出 Hasse 图边。
