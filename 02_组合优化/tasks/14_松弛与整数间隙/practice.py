"""第 14 晚：C5 顶点覆盖 LP 顶点枚举、整数 gap 与 1/2 舍入。"""
from __future__ import annotations
import sys
sys.stdout.reconfigure(encoding="utf-8", errors="backslashreplace")

from fractions import Fraction as F
from itertools import combinations, product


def solve_square(a: list[list[F]], b: list[F]) -> tuple[F, ...] | None:
    n = len(b)
    aug = [row[:] + [rhs] for row, rhs in zip(a, b)]
    for col in range(n):
        pivot = next((r for r in range(col, n) if aug[r][col]), None)
        if pivot is None:
            return None
        aug[col], aug[pivot] = aug[pivot], aug[col]
        scale = aug[col][col]
        aug[col] = [x / scale for x in aug[col]]
        for r in range(n):
            if r != col:
                factor = aug[r][col]
                aug[r] = [x - factor * y for x, y in zip(aug[r], aug[col])]
    return tuple(row[-1] for row in aug)


def lp_vertices(n: int, edges: list[tuple[int, int]]) -> set[tuple[F, ...]]:
    # 全部写成 a*x <= rhs。
    inequalities: list[tuple[list[F], F]] = []
    for u, v in edges:
        row = [F(0)] * n
        row[u] = row[v] = F(-1)
        inequalities.append((row, F(-1)))
    for i in range(n):
        lower = [F(0)] * n
        lower[i] = F(-1)
        inequalities.append((lower, F(0)))
        upper = [F(0)] * n
        upper[i] = F(1)
        inequalities.append((upper, F(1)))
    result: set[tuple[F, ...]] = set()
    for active in combinations(inequalities, n):
        point = solve_square([row for row, _ in active], [rhs for _, rhs in active])
        if point is not None and all(
            sum(a * x for a, x in zip(row, point)) <= rhs
            for row, rhs in inequalities
        ):
            result.add(point)
    return result


def is_cover(bits: tuple[int, ...], edges: list[tuple[int, int]]) -> bool:
    return all(bits[u] or bits[v] for u, v in edges)


def main() -> None:
    n = 5
    edges = [(i, (i + 1) % n) for i in range(n)]
    verts = lp_vertices(n, edges)
    lp = min(verts, key=sum)
    lp_value = sum(lp)
    integer_candidates = [bits for bits in product((0, 1), repeat=n) if is_cover(bits, edges)]
    integer = min(integer_candidates, key=sum)
    rounded = tuple(int(x >= F(1, 2)) for x in lp)
    assert lp == (F(1, 2),) * 5 and lp_value == F(5, 2)
    assert sum(integer) == 3 and is_cover(integer, edges)
    assert is_cover(rounded, edges)
    assert lp_value <= sum(integer) <= sum(rounded) <= 2 * lp_value
    print("LP solution =", lp, "value =", lp_value)
    print("IP optimum =", integer, "value =", sum(integer))
    print("rounded =", rounded, "value =", sum(rounded))
    print("integrality ratio =", float(F(sum(integer), 1) / lp_value))


if __name__ == "__main__":
    main()

# 动手改造：
# 1. 换成 K5，观察基本 LP gap 更接近 2。
# 2. 加权顶点覆盖仍按 1/2 舍入，核验 weighted cost <= 2 LP。
