"""第 28 晚：带 presolve、greedy、dual bound 的 mini set-cover 求解器。"""
from __future__ import annotations
import sys
sys.stdout.reconfigure(encoding="utf-8", errors="backslashreplace")

from dataclasses import dataclass
import heapq
from itertools import product
import math

UNIVERSE = frozenset(range(10))
COVER = {
    "A": frozenset({0, 1, 2}),
    "B": frozenset({2, 3, 4}),
    "C": frozenset({4, 5, 6}),
    "D": frozenset({6, 7, 8}),
    "E": frozenset({0, 3, 6}),
    "F": frozenset({1, 4, 7}),
    "G": frozenset({2, 5, 8}),
    "H": frozenset({0, 1}),       # 被 A 支配
    "I": frozenset({7, 8}),       # 被 D 支配
    "J": frozenset({3, 5}),
    "K": frozenset({8, 9}),       # 元素 9 强制 K
}
COST = {"A": 4, "B": 4, "C": 4, "D": 4, "E": 5, "F": 5,
        "G": 5, "H": 5, "I": 5, "J": 3, "K": 2}


def presolve() -> tuple[tuple[str, ...], frozenset[str], list[str]]:
    active = set(COVER)
    log = []
    for i in sorted(COVER):
        if i not in active:
            continue
        for j in sorted(COVER):
            if i == j or j not in active:
                continue
            if COVER[i] <= COVER[j] and COST[j] <= COST[i] and (
                COVER[i] < COVER[j] or COST[j] < COST[i]
            ):
                active.remove(i)
                log.append(f"dominated {i} by {j}")
                break
    forced: set[str] = set()
    covered: set[int] = set()
    changed = True
    while changed:
        changed = False
        for e in UNIVERSE - covered:
            candidates = [s for s in active if e in COVER[s]]
            if not candidates:
                raise ValueError(f"element {e} cannot be covered")
            if len(candidates) == 1:
                s = candidates[0]
                if s not in forced:
                    forced.add(s)
                    covered |= COVER[s]
                    log.append(f"forced {s} by element {e}")
                    changed = True
    return tuple(sorted(active)), frozenset(forced), log


def covered_by(chosen: frozenset[str]) -> frozenset[int]:
    return frozenset().union(*(COVER[s] for s in chosen)) if chosen else frozenset()


def greedy_completion(chosen: frozenset[str], active: tuple[str, ...]) -> frozenset[str]:
    result = set(chosen)
    covered = set(covered_by(chosen))
    while covered != set(UNIVERSE):
        s = min(
            (x for x in active if x not in result and COVER[x] - covered),
            key=lambda x: (COST[x] / len(COVER[x] - covered), x),
        )
        result.add(s)
        covered |= COVER[s]
    return frozenset(result)


def dual_lower_bound(uncovered: frozenset[int], available: tuple[str, ...]) -> float:
    """构造 set-cover LP 的显式 dual 可行 y，返回 sum(y)。"""
    residual = {s: float(COST[s]) for s in available}
    dual = {e: 0.0 for e in uncovered}
    for e in sorted(uncovered, key=lambda x: sum(x in COVER[s] for s in available)):
        candidates = [s for s in available if e in COVER[s]]
        if not candidates:
            return math.inf
        delta = min(residual[s] for s in candidates)
        dual[e] += delta
        for s in candidates:
            residual[s] -= delta
    assert all(
        sum(dual.get(e, 0.0) for e in COVER[s]) <= COST[s] + 1e-9
        for s in available
    )
    return sum(dual.values())


def solve() -> tuple[int, frozenset[str], dict[str, int], list[str]]:
    active, forced, prelog = presolve()
    incumbent = greedy_completion(forced, active)
    best_cost = sum(COST[s] for s in incumbent)
    stats = {"expanded": 0, "bound_pruned": 0, "deduplicated": 0}
    heap: list[tuple[float, int, frozenset[str]]] = []
    seen = {forced}
    counter = 0

    def bound(chosen: frozenset[str]) -> float:
        uncovered = UNIVERSE - covered_by(chosen)
        available = tuple(s for s in active if s not in chosen)
        return sum(COST[s] for s in chosen) + dual_lower_bound(uncovered, available)

    heapq.heappush(heap, (bound(forced), counter, forced))
    while heap:
        lower, _, chosen = heapq.heappop(heap)
        if lower >= best_cost - 1e-9:
            stats["bound_pruned"] += 1
            continue
        uncovered = UNIVERSE - covered_by(chosen)
        if not uncovered:
            best_cost, incumbent = sum(COST[s] for s in chosen), chosen
            continue
        stats["expanded"] += 1
        available = tuple(s for s in active if s not in chosen)
        pivot = min(uncovered, key=lambda e: sum(e in COVER[s] for s in available))
        for s in available:
            if pivot not in COVER[s]:
                continue
            child = chosen | {s}
            if child in seen:
                stats["deduplicated"] += 1
                continue
            seen.add(child)
            heuristic = greedy_completion(child, active)
            hcost = sum(COST[x] for x in heuristic)
            if hcost < best_cost:
                best_cost, incumbent = hcost, heuristic
            child_bound = bound(child)
            if child_bound < best_cost - 1e-9:
                counter += 1
                heapq.heappush(heap, (child_bound, counter, child))
            else:
                stats["bound_pruned"] += 1
    return best_cost, incumbent, stats, prelog


def brute() -> tuple[int, frozenset[str]]:
    names = tuple(COVER)
    best = (10**9, frozenset())
    for bits in product((0, 1), repeat=len(names)):
        chosen = frozenset(s for s, b in zip(names, bits) if b)
        if covered_by(chosen) == UNIVERSE:
            candidate = (sum(COST[s] for s in chosen), chosen)
            if candidate[0] < best[0]:
                best = candidate
    return best


def main() -> None:
    value, chosen, stats, prelog = solve()
    truth, _ = brute()
    assert covered_by(chosen) == UNIVERSE
    assert sum(COST[s] for s in chosen) == value == truth
    assert any("dominated" in line for line in prelog)
    assert any("forced" in line for line in prelog)
    print("presolve =", prelog)
    print("optimum =", value, "sets =", sorted(chosen))
    print("search stats =", stats, "full binary candidates =", 2 ** len(COVER))


if __name__ == "__main__":
    main()

# 动手改造：
# 1. 关闭 presolve/greedy/dual bound 各跑一次，做 ablation 节点表。
# 2. 输出 TIME_LIMIT 模拟状态：incumbent、开放节点最小 bound 与 gap。
