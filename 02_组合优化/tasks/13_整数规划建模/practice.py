"""第 13 晚：有容量设施选址的精确枚举与独立模型检查。"""
from __future__ import annotations
import sys
sys.stdout.reconfigure(encoding="utf-8", errors="backslashreplace")

from itertools import product

FIXED = [6, 5, 4]
CAPACITY = [2, 3, 2]
SERVICE = [
    [2, 6, 5],  # customer 0 -> facilities
    [4, 2, 6],
    [5, 3, 2],
    [7, 4, 1],
]


def check(opened: tuple[int, ...], assignment: tuple[int, ...]) -> tuple[bool, str]:
    if len(opened) != len(FIXED) or any(x not in (0, 1) for x in opened):
        return False, "invalid y"
    if len(assignment) != len(SERVICE):
        return False, "each customer needs one assignment"
    load = [0] * len(FIXED)
    for i, j in enumerate(assignment):
        if not (0 <= j < len(FIXED)):
            return False, f"customer {i}: invalid facility"
        if not opened[j]:
            return False, f"customer {i}: assigned to closed facility {j}"
        load[j] += 1
    if any(load[j] > CAPACITY[j] for j in range(len(FIXED))):
        return False, f"capacity exceeded: {load}"
    return True, "ok"


def cost(opened: tuple[int, ...], assignment: tuple[int, ...]) -> int:
    return sum(f * y for f, y in zip(FIXED, opened)) + sum(
        SERVICE[i][j] for i, j in enumerate(assignment)
    )


def exact_solve() -> tuple[int, tuple[int, ...], tuple[int, ...], int]:
    best = (10**9, (), ())
    checked = 0
    for opened in product((0, 1), repeat=len(FIXED)):
        if not any(opened):
            continue
        for assignment in product(range(len(FIXED)), repeat=len(SERVICE)):
            checked += 1
            if check(opened, assignment)[0]:
                candidate = (cost(opened, assignment), opened, assignment)
                if candidate < best:
                    best = candidate
    return best[0], best[1], best[2], checked


def cheapest_open_greedy() -> tuple[int, tuple[int, ...], tuple[int, ...]]:
    # 先按固定成本开设施，直到总容量够；再逐客户选有余量的最低服务费。
    order = sorted(range(len(FIXED)), key=lambda j: FIXED[j])
    opened = [0] * len(FIXED)
    for j in order:
        opened[j] = 1
        if sum(CAPACITY[k] for k, y in enumerate(opened) if y) >= len(SERVICE):
            break
    load = [0] * len(FIXED)
    assignment = []
    for row in SERVICE:
        j = min(
            (k for k, y in enumerate(opened) if y and load[k] < CAPACITY[k]),
            key=lambda k: row[k],
        )
        assignment.append(j)
        load[j] += 1
    o, a = tuple(opened), tuple(assignment)
    assert check(o, a)[0]
    return cost(o, a), o, a


def main() -> None:
    optimum, opened, assignment, checked = exact_solve()
    assert check(opened, assignment)[0]
    assert cost(opened, assignment) == optimum == 19
    assert not check((0, 1, 1), (0, 1, 2, 2))[0]
    heuristic, ho, ha = cheapest_open_greedy()
    assert heuristic >= optimum and check(ho, ha)[0]
    print("checked candidates =", checked)
    print("optimum =", optimum, "open =", opened, "assignment =", assignment)
    print("greedy upper bound =", heuristic, "open =", ho, "assignment =", ha)


if __name__ == "__main__":
    main()

# 动手改造：
# 1. 允许客户需求大于 1，并把容量检查改为需求加总。
# 2. 输出聚合 linking 松弛可行、分解 linking 不可行的分数点。
