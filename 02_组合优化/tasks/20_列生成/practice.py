"""第 20 晚：切割库存的 restricted master dual + pricing 列生成。"""
from __future__ import annotations
import sys
sys.stdout.reconfigure(encoding="utf-8", errors="backslashreplace")

from collections import deque
from fractions import Fraction as F
from itertools import combinations, product
import math

LENGTH = 10
SIZES = (4, 3, 2)
DEMAND = (4, 5, 6)
Pattern = tuple[int, ...]


def all_patterns() -> list[Pattern]:
    patterns = []
    ranges = [range(LENGTH // size + 1) for size in SIZES]
    for p in product(*ranges):
        if any(p) and sum(a * w for a, w in zip(p, SIZES)) <= LENGTH:
            patterns.append(p)
    return sorted(patterns)


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


def restricted_dual(patterns: list[Pattern]) -> tuple[tuple[F, ...], F]:
    # pattern*y <= 1, y>=0。
    inequalities = [(tuple(map(F, p)), F(1)) for p in patterns]
    inequalities += [
        (tuple(F(-1) if i == j else F(0) for i in range(3)), F(0))
        for j in range(3)
    ]
    verts = set()
    for active in combinations(inequalities, 3):
        y = solve_square([list(a) for a, _ in active], [b for _, b in active])
        if y is not None and all(sum(ai * yi for ai, yi in zip(a, y)) <= b for a, b in inequalities):
            verts.add(y)
    if not verts:
        raise RuntimeError("restricted dual has no vertex")
    y = max(verts, key=lambda z: sum(F(d) * zi for d, zi in zip(DEMAND, z)))
    return y, sum(F(d) * yi for d, yi in zip(DEMAND, y))


def integer_cover_dp(patterns: list[Pattern]) -> tuple[int, list[Pattern]]:
    start = (0, 0, 0)
    target = DEMAND
    distance = {start: 0}
    parent: dict[Pattern, tuple[Pattern, Pattern]] = {}
    q = deque([start])
    while q:
        state = q.popleft()
        if state == target:
            break
        for p in patterns:
            nxt = tuple(min(d, s + a) for d, s, a in zip(target, state, p))
            if nxt not in distance:
                distance[nxt] = distance[state] + 1
                parent[nxt] = (state, p)
                q.append(nxt)
    plan, cur = [], target
    while cur != start:
        cur, p = parent[cur]
        plan.append(p)
    plan.reverse()
    return distance[target], plan


def main() -> None:
    universe = all_patterns()
    columns = [
        tuple(LENGTH // SIZES[i] if i == j else 0 for i in range(3))
        for j in range(3)
    ]
    log = []
    for iteration in range(20):
        dual, value = restricted_dual(columns)
        priced = max(universe, key=lambda p: sum(F(a) * y for a, y in zip(p, dual)))
        price = sum(F(a) * y for a, y in zip(priced, dual))
        log.append((iteration, dual, value, priced, price))
        if price <= 1:
            break
        assert priced not in columns
        columns.append(priced)
    else:
        raise AssertionError("column generation did not converge")
    assert all(sum(F(a) * y for a, y in zip(p, dual)) <= 1 for p in universe)
    rolls, plan = integer_cover_dp(universe)
    coverage = tuple(sum(p[i] for p in plan) for i in range(3))
    assert all(c >= d for c, d in zip(coverage, DEMAND))
    assert math.ceil(value) <= rolls
    print("iterations:")
    for row in log:
        print(row)
    print("final LP lower bound =", value, "generated columns =", columns)
    print("integer plan rolls =", rolls, "coverage =", coverage, "patterns =", plan)


if __name__ == "__main__":
    main()

# 动手改造：
# 1. 一轮加入所有 price>1+epsilon 的列，比较迭代数与列数。
# 2. 只用生成列做整数 DP，与全 pattern DP 比较，观察“price-and-branch”缺口。
