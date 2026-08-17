"""第 24 晚：最近邻、2-opt descent 与可复现模拟退火。"""
from __future__ import annotations
import sys
sys.stdout.reconfigure(encoding="utf-8", errors="backslashreplace")

import math
import random

Point = tuple[float, float]


def matrix(points: list[Point]) -> list[list[float]]:
    return [[math.hypot(a[0] - b[0], a[1] - b[1]) for b in points] for a in points]


def length(tour: list[int], d: list[list[float]]) -> float:
    return sum(d[tour[i]][tour[(i + 1) % len(tour)]] for i in range(len(tour)))


def check_tour(tour: list[int], n: int) -> None:
    assert len(tour) == n and tour[0] == 0 and sorted(tour) == list(range(n))


def nearest_neighbor(d: list[list[float]]) -> list[int]:
    tour, unused = [0], set(range(1, len(d)))
    while unused:
        nxt = min(unused, key=lambda v: (d[tour[-1]][v], v))
        tour.append(nxt)
        unused.remove(nxt)
    return tour


def two_opt(tour: list[int], d: list[list[float]]) -> tuple[list[int], int]:
    tour = tour[:]
    moves = 0
    while True:
        improved = False
        for i in range(1, len(tour) - 1):
            for k in range(i + 1, len(tour)):
                a, b = tour[i - 1], tour[i]
                c, e = tour[k], tour[(k + 1) % len(tour)]
                delta = d[a][c] + d[b][e] - d[a][b] - d[c][e]
                if delta < -1e-12:
                    tour[i:k + 1] = reversed(tour[i:k + 1])
                    moves += 1
                    improved = True
                    break
            if improved:
                break
        if not improved:
            return tour, moves


def simulated_annealing(
    start: list[int], d: list[list[float]], seed: int, iterations: int = 8000
) -> tuple[list[int], float, int]:
    rng = random.Random(seed)
    current = start[:]
    current_value = length(current, d)
    best, best_value = current[:], current_value
    temperature = current_value / len(current)
    accepted_worse = 0
    for _ in range(iterations):
        i, k = sorted(rng.sample(range(1, len(current)), 2))
        a, b = current[i - 1], current[i]
        c, e = current[k], current[(k + 1) % len(current)]
        delta = d[a][c] + d[b][e] - d[a][b] - d[c][e]
        if delta <= 0 or rng.random() < math.exp(-delta / max(temperature, 1e-12)):
            current[i:k + 1] = reversed(current[i:k + 1])
            current_value += delta
            accepted_worse += int(delta > 0)
            if current_value < best_value:
                best, best_value = current[:], current_value
        temperature *= 0.9994
    return best, best_value, accepted_worse


def main() -> None:
    rng = random.Random(20260813)
    points = [(rng.random() * 100, rng.random() * 100) for _ in range(18)]
    d = matrix(points)
    nn = nearest_neighbor(d)
    local, moves = two_opt(nn, d)
    annealed, reported, worse = simulated_annealing(local, d, seed=17)
    for tour in (nn, local, annealed):
        check_tour(tour, len(points))
    nn_value, local_value, annealed_value = map(lambda t: length(t, d), (nn, local, annealed))
    assert local_value <= nn_value + 1e-9
    assert annealed_value <= local_value + 1e-9
    assert math.isclose(reported, annealed_value, rel_tol=1e-10, abs_tol=1e-8)
    print("nearest-neighbor =", round(nn_value, 3))
    print("2-opt =", round(local_value, 3), "improving moves =", moves)
    print("annealing best =", round(annealed_value, 3), "accepted worse moves =", worse)


if __name__ == "__main__":
    main()

# 动手改造：
# 1. 用 10 个种子报告 min/median/max，而非只挑最好一次。
# 2. 实现 double-bridge perturbation + 2-opt 的 iterated local search。
