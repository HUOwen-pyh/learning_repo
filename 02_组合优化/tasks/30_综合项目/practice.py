"""第 30 晚：抗单设施中断的有容量设施选址综合项目。"""
from __future__ import annotations
import sys
sys.stdout.reconfigure(encoding="utf-8", errors="backslashreplace")

from itertools import product
import math

FIXED = (7, 8, 6, 9)
CAPACITY = (3, 3, 3, 3)
SERVICE = (
    (1, 6, 8, 9),
    (2, 5, 7, 8),
    (6, 1, 5, 7),
    (7, 2, 4, 6),
    (8, 6, 1, 3),
    (9, 7, 2, 1),
)
SCENARIOS: tuple[int | None, ...] = (None, 0, 1, 2, 3)


def check_assignment(
    opened: tuple[int, ...], failed: int | None, assignment: tuple[int, ...]
) -> bool:
    if len(assignment) != len(SERVICE):
        return False
    load = [0] * len(FIXED)
    for i, j in enumerate(assignment):
        if not (0 <= j < len(FIXED)) or not opened[j] or j == failed:
            return False
        load[j] += 1
    return all(load[j] <= CAPACITY[j] for j in range(len(FIXED)))


def best_assignment(
    opened: tuple[int, ...], failed: int | None
) -> tuple[int, tuple[int, ...]] | None:
    available = [j for j, y in enumerate(opened) if y and j != failed]
    if sum(CAPACITY[j] for j in available) < len(SERVICE):
        return None
    best = (math.inf, ())
    for assignment in product(available, repeat=len(SERVICE)):
        if not check_assignment(opened, failed, assignment):
            continue
        value = sum(SERVICE[i][j] for i, j in enumerate(assignment))
        if value < best[0]:
            best = (value, assignment)
    return None if math.isinf(best[0]) else (int(best[0]), best[1])


def evaluate(
    opened: tuple[int, ...],
) -> tuple[int, int | None, dict[int | None, tuple[int, tuple[int, ...]]]] | None:
    recourse = {}
    for failed in SCENARIOS:
        result = best_assignment(opened, failed)
        if result is None:
            return None
        recourse[failed] = result
    worst_scenario = max(SCENARIOS, key=lambda s: recourse[s][0])
    objective = sum(f * y for f, y in zip(FIXED, opened)) + recourse[worst_scenario][0]
    return objective, worst_scenario, recourse


def exact() -> tuple[int, tuple[int, ...], int | None, dict[int | None, tuple[int, tuple[int, ...]]]]:
    candidates = []
    for opened in product((0, 1), repeat=len(FIXED)):
        result = evaluate(opened)
        if result:
            candidates.append((result[0], opened, result[1], result[2]))
    return min(candidates, key=lambda row: row[0])


def relaxed_lower_bound() -> int:
    """忽略每设施容量，但保留开放/故障和每客户一次，故是可靠 LB。"""
    best = math.inf
    for opened in product((0, 1), repeat=len(FIXED)):
        scenario_costs = []
        valid = True
        for failed in SCENARIOS:
            available = [j for j, y in enumerate(opened) if y and j != failed]
            if not available:
                valid = False
                break
            scenario_costs.append(sum(min(row[j] for j in available) for row in SERVICE))
        if valid:
            value = sum(f * y for f, y in zip(FIXED, opened)) + max(scenario_costs)
            best = min(best, value)
    return int(best)


def drop_heuristic() -> tuple[int, tuple[int, ...]]:
    opened = (1,) * len(FIXED)
    current = evaluate(opened)
    assert current is not None
    while True:
        moves = []
        for j, y in enumerate(opened):
            if not y:
                continue
            candidate = tuple(0 if i == j else x for i, x in enumerate(opened))
            result = evaluate(candidate)
            if result:
                moves.append((result[0], candidate))
        if not moves:
            break
        best_move = min(moves)
        if best_move[0] >= current[0]:
            break
        opened = best_move[1]
        current = evaluate(opened)
        assert current is not None
    return current[0], opened


def main() -> None:
    optimum, opened, worst, recourse = exact()
    lower = relaxed_lower_bound()
    heuristic, h_opened = drop_heuristic()
    assert lower <= optimum <= heuristic
    for failed, (service, assignment) in recourse.items():
        assert check_assignment(opened, failed, assignment)
        assert service == sum(SERVICE[i][j] for i, j in enumerate(assignment))
    assert optimum == sum(f * y for f, y in zip(FIXED, opened)) + recourse[worst][0]
    print("relaxation LB =", lower)
    print("exact objective =", optimum, "open =", opened, "worst scenario =", worst)
    for failed in SCENARIOS:
        print("scenario failed =", failed, "service/assignment =", recourse[failed])
    print("drop heuristic UB =", heuristic, "open =", h_opened)


if __name__ == "__main__":
    main()

# 动手改造：
# 1. 将一个设施容量降为 2，重跑并解释 robust opening 的变化。
# 2. 只按需加入当前最坏故障情景，模拟 constraint generation。
