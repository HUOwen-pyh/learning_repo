"""第 11 晚：有理数 LP primal/dual 顶点与互补松弛证书。"""
from __future__ import annotations
import sys
sys.stdout.reconfigure(encoding="utf-8", errors="backslashreplace")

from fractions import Fraction as F
from itertools import combinations

Inequality = tuple[tuple[F, ...], F, str]  # a*x <= rhs


def solve_square(a: list[list[F]], b: list[F]) -> tuple[F, ...] | None:
    n = len(b)
    aug = [row[:] + [rhs] for row, rhs in zip(a, b)]
    for col in range(n):
        pivot = next((r for r in range(col, n) if aug[r][col] != 0), None)
        if pivot is None:
            return None
        aug[col], aug[pivot] = aug[pivot], aug[col]
        scale = aug[col][col]
        aug[col] = [x / scale for x in aug[col]]
        for r in range(n):
            if r == col:
                continue
            factor = aug[r][col]
            aug[r] = [x - factor * y for x, y in zip(aug[r], aug[col])]
    return tuple(aug[i][-1] for i in range(n))


def dot(a: tuple[F, ...], x: tuple[F, ...]) -> F:
    return sum((ai * xi for ai, xi in zip(a, x)), F(0))


def vertices(dim: int, inequalities: list[Inequality]) -> set[tuple[F, ...]]:
    ans: set[tuple[F, ...]] = set()
    for active in combinations(inequalities, dim):
        point = solve_square([list(row) for row, _, _ in active], [rhs for _, rhs, _ in active])
        if point is not None and all(dot(row, point) <= rhs for row, rhs, _ in inequalities):
            ans.add(point)
    return ans


def main() -> None:
    primal: list[Inequality] = [
        ((F(1), F(1)), F(4), "resource-1"),
        ((F(2), F(1)), F(5), "resource-2"),
        ((F(1), F(0)), F(5, 2), "x-cap"),
        ((F(-1), F(0)), F(0), "x>=0"),
        ((F(0), F(-1)), F(0), "y>=0"),
    ]
    pverts = vertices(2, primal)
    px = max(pverts, key=lambda x: 3 * x[0] + 2 * x[1])
    pvalue = 3 * px[0] + 2 * px[1]

    # dual: min 4y1+5y2+2.5y3; A^T y >= c, y>=0。
    dual: list[Inequality] = [
        ((F(-1), F(-2), F(-1)), F(-3), "x-column"),
        ((F(-1), F(-1), F(0)), F(-2), "y-column"),
        ((F(-1), F(0), F(0)), F(0), "y1>=0"),
        ((F(0), F(-1), F(0)), F(0), "y2>=0"),
        ((F(0), F(0), F(-1)), F(0), "y3>=0"),
    ]
    dverts = vertices(3, dual)
    dy = min(dverts, key=lambda y: 4 * y[0] + 5 * y[1] + F(5, 2) * y[2])
    dvalue = 4 * dy[0] + 5 * dy[1] + F(5, 2) * dy[2]
    assert px == (F(1), F(3)) and dy == (F(1), F(1), F(0))
    assert pvalue == dvalue == 9

    primal_slack = [F(4) - px[0] - px[1], F(5) - 2 * px[0] - px[1], F(5, 2) - px[0]]
    dual_slack = [dy[0] + 2 * dy[1] + dy[2] - 3, dy[0] + dy[1] - 2]
    assert all(mult * slack == 0 for mult, slack in zip(dy, primal_slack))
    assert all(var * slack == 0 for var, slack in zip(px, dual_slack))
    print("primal x =", px, "value =", pvalue, "slacks =", primal_slack)
    print("dual y =", dy, "value =", dvalue, "slacks =", dual_slack)
    print("strong duality and complementary slackness: verified")


if __name__ == "__main__":
    main()

# 动手改造：
# 1. 改变目标系数，让 x=0，观察对应 dual 约束可不紧。
# 2. 为矛盾系统 x<=0, x>=1 手写并核验一个 Farkas 乘子。
