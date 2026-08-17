"""第 21 晚：连续供货 recourse 的经典 Benders cut loop。"""
from __future__ import annotations
import sys
sys.stdout.reconfigure(encoding="utf-8", errors="backslashreplace")

from fractions import Fraction as F
from itertools import product
import math

FIXED = (4, 5, 6)
CAPACITY = (5, 5, 5)
UNIT_COST = (5, 2, 4)
DEMAND = 8
Cut = tuple[F, tuple[F, ...]]  # alpha, beta；theta >= D*alpha-sum(cap*y*beta)


def subproblem(opened: tuple[int, ...]) -> tuple[F, Cut, tuple[F, ...]] | None:
    if sum(c * y for c, y in zip(CAPACITY, opened)) < DEMAND:
        return None
    remain = F(DEMAND)
    shipped = [F(0)] * len(opened)
    marginal = None
    for j in sorted(range(len(opened)), key=lambda i: UNIT_COST[i]):
        if not opened[j]:
            continue
        amount = min(F(CAPACITY[j]), remain)
        shipped[j] = amount
        remain -= amount
        if amount:
            marginal = F(UNIT_COST[j])
        if remain == 0:
            break
    assert marginal is not None and remain == 0
    alpha = marginal
    beta = tuple(max(F(0), alpha - F(c)) for c in UNIT_COST)
    recourse = sum(q * c for q, c in zip(shipped, UNIT_COST))
    dual_value = F(DEMAND) * alpha - sum(
        F(cap * y) * b for cap, y, b in zip(CAPACITY, opened, beta)
    )
    assert recourse == dual_value
    return recourse, (alpha, beta), tuple(shipped)


def cut_value(cut: Cut, opened: tuple[int, ...]) -> F:
    alpha, beta = cut
    return F(DEMAND) * alpha - sum(
        F(cap * y) * b for cap, y, b in zip(CAPACITY, opened, beta)
    )


def master(cuts: list[Cut], capacity_cut: bool) -> tuple[F, tuple[int, ...], F]:
    best = (F(10**9), (), F(0))
    for opened in product((0, 1), repeat=len(FIXED)):
        if capacity_cut and sum(c * y for c, y in zip(CAPACITY, opened)) < DEMAND:
            continue
        theta = max([F(0)] + [cut_value(cut, opened) for cut in cuts])
        candidate = F(sum(f * y for f, y in zip(FIXED, opened))) + theta
        if candidate < best[0]:
            best = candidate, opened, theta
    return best


def full_enumeration() -> tuple[F, tuple[int, ...]]:
    candidates = []
    for opened in product((0, 1), repeat=len(FIXED)):
        result = subproblem(opened)
        if result:
            candidates.append((F(sum(f * y for f, y in zip(FIXED, opened))) + result[0], opened))
    return min(candidates)


def main() -> None:
    cuts: list[Cut] = []
    capacity_cut = False
    upper = F(10**9)
    incumbent: tuple[int, ...] = ()
    log = []
    last_lower = F(-1)
    for iteration in range(20):
        lower, opened, theta = master(cuts, capacity_cut)
        assert lower >= last_lower
        last_lower = lower
        result = subproblem(opened)
        if result is None:
            capacity_cut = True
            log.append((iteration, opened, lower, "feasibility cut"))
            continue
        recourse, cut, shipped = result
        actual = F(sum(f * y for f, y in zip(FIXED, opened))) + recourse
        if actual < upper:
            upper, incumbent = actual, opened
        # dual cut 必须对每个可行开设集合给出 recourse 下界。
        for y in product((0, 1), repeat=len(FIXED)):
            q = subproblem(y)
            if q:
                assert cut_value(cut, y) <= q[0]
        cuts.append(cut)
        log.append((iteration, opened, lower, theta, recourse, shipped, upper))
        new_lower = master(cuts, capacity_cut)[0]
        if new_lower >= upper:
            last_lower = new_lower
            break
    truth, truth_y = full_enumeration()
    assert last_lower == upper == truth == 33
    assert incumbent == truth_y == (0, 1, 1)
    print("Benders log:")
    for row in log:
        print(row)
    print("LB = UB =", upper, "open =", incumbent, "cuts =", len(cuts))


if __name__ == "__main__":
    main()

# 动手改造：
# 1. 把需求改成多个情景，比较 single-cut 与 multi-cut。
# 2. 加入“至少开一个指定区域设施”的 master 约束，观察子问题不变。
