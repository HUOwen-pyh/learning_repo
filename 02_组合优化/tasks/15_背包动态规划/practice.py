"""第 15 晚：0-1 背包精确 DP 与价值缩放 FPTAS。"""
from __future__ import annotations
import sys
sys.stdout.reconfigure(encoding="utf-8", errors="backslashreplace")

from dataclasses import dataclass
import math


@dataclass(frozen=True)
class Item:
    name: str
    weight: int
    value: int


ITEMS = [
    Item("A", 12, 24), Item("B", 7, 13), Item("C", 11, 23),
    Item("D", 8, 15), Item("E", 9, 16), Item("F", 4, 7),
]
CAPACITY = 26


def exact_knapsack(items: list[Item], capacity: int) -> tuple[int, list[int]]:
    n = len(items)
    dp = [[0] * (capacity + 1) for _ in range(n + 1)]
    for i, item in enumerate(items, 1):
        for b in range(capacity + 1):
            dp[i][b] = dp[i - 1][b]
            if item.weight <= b:
                dp[i][b] = max(dp[i][b], dp[i - 1][b - item.weight] + item.value)
    chosen: list[int] = []
    b = capacity
    for i in range(n, 0, -1):
        if dp[i][b] != dp[i - 1][b]:
            chosen.append(i - 1)
            b -= items[i - 1].weight
    chosen.reverse()
    return dp[n][capacity], chosen


def fptas(items: list[Item], capacity: int, epsilon: float) -> tuple[int, list[int], int]:
    if not 0 < epsilon < 1:
        raise ValueError("epsilon must be in (0,1)")
    n = len(items)
    scale = epsilon * max(item.value for item in items) / n
    scaled = [math.floor(item.value / scale) for item in items]
    total = sum(scaled)
    inf = 10**18
    dp = [[inf] * (total + 1) for _ in range(n + 1)]
    dp[0][0] = 0
    for i, item in enumerate(items, 1):
        sv = scaled[i - 1]
        for p in range(total + 1):
            dp[i][p] = dp[i - 1][p]
            if p >= sv and dp[i - 1][p - sv] + item.weight < dp[i][p]:
                dp[i][p] = dp[i - 1][p - sv] + item.weight
    best_p = max(p for p, weight in enumerate(dp[n]) if weight <= capacity)
    chosen: list[int] = []
    p = best_p
    for i in range(n, 0, -1):
        sv = scaled[i - 1]
        if p >= sv and dp[i][p] == dp[i - 1][p - sv] + items[i - 1].weight:
            chosen.append(i - 1)
            p -= sv
    chosen.reverse()
    actual = sum(items[i].value for i in chosen)
    return actual, chosen, total


def verify(chosen: list[int]) -> tuple[int, int]:
    assert len(chosen) == len(set(chosen))
    return (
        sum(ITEMS[i].weight for i in chosen),
        sum(ITEMS[i].value for i in chosen),
    )


def main() -> None:
    optimum, exact_items = exact_knapsack(ITEMS, CAPACITY)
    ew, ev = verify(exact_items)
    assert ew <= CAPACITY and ev == optimum
    print("exact =", optimum, [ITEMS[i].name for i in exact_items], "weight =", ew)
    previous_states = 0
    for epsilon in (0.40, 0.20):
        approx, chosen, states = fptas(ITEMS, CAPACITY, epsilon)
        weight, value = verify(chosen)
        assert weight <= CAPACITY and value == approx
        assert approx + 1e-9 >= (1 - epsilon) * optimum
        assert states >= previous_states
        previous_states = states
        print(f"eps={epsilon:.2f}: value={approx}, items={[ITEMS[i].name for i in chosen]}, scaled_states={states}")


if __name__ == "__main__":
    main()

# 动手改造：
# 1. 用 Pareto frontier 删除被支配的 (weight,value) 状态。
# 2. 生成小随机实例，以穷举核对 DP，并绘制 epsilon/状态数表（文本即可）。
