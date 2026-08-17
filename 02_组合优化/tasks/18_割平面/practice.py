"""第 18 晚：二维 Chvatal-Gomory cut 与 0-1 cover cut 验证。"""
from __future__ import annotations
import sys
sys.stdout.reconfigure(encoding="utf-8", errors="backslashreplace")

from fractions import Fraction as F
from itertools import combinations, product
import math

Constraint = tuple[F, F, F, str]  # ax+by <= rhs


def intersect(p: Constraint, q: Constraint) -> tuple[F, F] | None:
    a, b, r, _ = p
    c, d, s, _ = q
    det = a * d - b * c
    return None if det == 0 else ((r * d - b * s) / det, (a * s - r * c) / det)


def vertices(cons: list[Constraint]) -> set[tuple[F, F]]:
    ans = set()
    for p, q in combinations(cons, 2):
        point = intersect(p, q)
        if point is not None and all(a * point[0] + b * point[1] <= r for a, b, r, _ in cons):
            ans.add(point)
    return ans


def make_cg_cut(rows: list[Constraint], multipliers: list[F]) -> Constraint:
    a = sum((u * row[0] for u, row in zip(multipliers, rows)), F(0))
    b = sum((u * row[1] for u, row in zip(multipliers, rows)), F(0))
    rhs = sum((u * row[2] for u, row in zip(multipliers, rows)), F(0))
    if a.denominator != 1 or b.denominator != 1:
        raise ValueError("CG 取整要求聚合后的左端系数为整数")
    return a, b, F(math.floor(rhs)), "CG cut"


def main() -> None:
    base: list[Constraint] = [
        (F(2), F(1), F(4), "2x+y<=4"),
        (F(1), F(2), F(4), "x+2y<=4"),
        (F(-1), F(0), F(0), "x>=0"),
        (F(0), F(-1), F(0), "y>=0"),
    ]
    lp_point = max(vertices(base), key=lambda p: p[0] + p[1])
    lp_value = sum(lp_point)
    integer = max(
        ((x + y, (x, y)) for x, y in product(range(5), repeat=2)
         if all(a * x + b * y <= rhs for a, b, rhs, _ in base)),
    )
    cut = make_cg_cut(base[:2], [F(1, 3), F(1, 3)])
    assert cut[:3] == (F(1), F(1), F(2))
    assert cut[0] * lp_point[0] + cut[1] * lp_point[1] > cut[2]
    # 小实例枚举验证：不删任何整数可行点。
    assert all(
        cut[0] * x + cut[1] * y <= cut[2]
        for x, y in product(range(5), repeat=2)
        if all(a * x + b * y <= rhs for a, b, rhs, _ in base)
    )
    cut_point = max(vertices(base + [cut]), key=lambda p: p[0] + p[1])
    assert lp_point == (F(4, 3), F(4, 3)) and lp_value == F(8, 3)
    assert integer[0] == 2 and sum(cut_point) == integer[0]

    weights, capacity, cover = [6, 5, 4], 10, {0, 1}
    assert sum(weights[i] for i in cover) > capacity
    assert all(
        sum(bits[i] for i in cover) <= len(cover) - 1
        for bits in product((0, 1), repeat=3)
        if sum(w * x for w, x in zip(weights, bits)) <= capacity
    )
    print("original LP =", lp_point, "value =", lp_value, "; IP value =", integer[0])
    print("generated cut =", cut[:3], "; new LP =", cut_point)
    print("cover cut: x0+x1<=1 verified on every feasible binary point")


if __name__ == "__main__":
    main()

# 动手改造：
# 1. 枚举小有理乘子，自动找最违反当前 LP 点的 CG cut。
# 2. 对 cover 做 sequential lifting，比较未提升/提升割的强度。
