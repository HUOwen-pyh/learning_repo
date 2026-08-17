"""第 29 晚：disjunctive graph 搜索求 3x3 job-shop 最优 makespan。"""
from __future__ import annotations
import sys
sys.stdout.reconfigure(encoding="utf-8", errors="backslashreplace")

from collections import deque
from dataclasses import dataclass
from itertools import combinations
import math


@dataclass(frozen=True)
class Operation:
    id: int
    job: int
    index: int
    machine: int
    duration: int


RAW_JOBS = [
    [(0, 3), (1, 2), (2, 2)],
    [(0, 2), (2, 1), (1, 4)],
    [(1, 4), (2, 3), (0, 1)],
]


def build() -> tuple[list[Operation], set[tuple[int, int]], list[tuple[int, int]]]:
    ops: list[Operation] = []
    by_job: list[list[int]] = []
    for j, job in enumerate(RAW_JOBS):
        ids = []
        for k, (machine, duration) in enumerate(job):
            ids.append(len(ops))
            ops.append(Operation(len(ops), j, k, machine, duration))
        by_job.append(ids)
    fixed = {(ids[k], ids[k + 1]) for ids in by_job for k in range(len(ids) - 1)}
    disjunctions = []
    for machine in range(3):
        machine_ops = [op.id for op in ops if op.machine == machine]
        disjunctions.extend(combinations(machine_ops, 2))
    return ops, fixed, disjunctions


def longest_path(
    ops: list[Operation], arcs: set[tuple[int, int]]
) -> tuple[int, list[int]] | None:
    out = [[] for _ in ops]
    indegree = [0] * len(ops)
    for u, v in arcs:
        out[u].append(v)
        indegree[v] += 1
    q = deque(i for i, d in enumerate(indegree) if d == 0)
    start = [0] * len(ops)
    seen = 0
    while q:
        u = q.popleft()
        seen += 1
        for v in out[u]:
            start[v] = max(start[v], start[u] + ops[u].duration)
            indegree[v] -= 1
            if indegree[v] == 0:
                q.append(v)
    if seen != len(ops):
        return None
    makespan = max(start[i] + ops[i].duration for i in range(len(ops)))
    return makespan, start


def solve() -> tuple[int, list[int], set[tuple[int, int]], dict[str, int]]:
    ops, fixed, pairs = build()
    best = math.inf
    best_start: list[int] = []
    best_arcs: set[tuple[int, int]] = set()
    stats = {"leaves": 0, "cycle_pruned": 0, "bound_pruned": 0}

    def dfs(k: int, arcs: set[tuple[int, int]]) -> None:
        nonlocal best, best_start, best_arcs
        state = longest_path(ops, arcs)
        if state is None:
            stats["cycle_pruned"] += 1
            return
        lower, starts = state
        if lower >= best:
            stats["bound_pruned"] += 1
            return
        if k == len(pairs):
            stats["leaves"] += 1
            best, best_start, best_arcs = lower, starts, set(arcs)
            return
        a, b = pairs[k]
        dfs(k + 1, arcs | {(a, b)})
        dfs(k + 1, arcs | {(b, a)})

    dfs(0, fixed)
    return int(best), best_start, best_arcs, stats


def verify(makespan: int, start: list[int]) -> None:
    ops, _, _ = build()
    assert all(s >= 0 and s + op.duration <= makespan for s, op in zip(start, ops))
    for a, b in zip(ops, ops[1:]):
        if a.job == b.job:
            assert start[a.id] + a.duration <= start[b.id]
    for a, b in combinations(ops, 2):
        if a.machine == b.machine:
            assert (
                start[a.id] + a.duration <= start[b.id]
                or start[b.id] + b.duration <= start[a.id]
            )


def main() -> None:
    makespan, start, arcs, stats = solve()
    ops, _, _ = build()
    verify(makespan, start)
    assert makespan == 11
    assert stats["cycle_pruned"] > 0 and stats["bound_pruned"] > 0
    print("optimal makespan =", makespan)
    print("schedule =", [(op.job, op.index, op.machine, start[op.id], op.duration) for op in ops])
    print("oriented arcs =", len(arcs), "search stats =", stats)


if __name__ == "__main__":
    main()

# 动手改造：
# 1. 先分支 critical path 上的机器冲突，比较节点数。
# 2. 加 release date 或 optional operation，并写对应 checker。
