"""加权 Set Cover：单位新覆盖成本贪心、bitmask 精确 DP、H_n 断言。"""
from math import fsum
from random import Random


def greedy_cover(n, sets, costs):
    uncovered, picked, charges = set(range(n)), [], [0.0] * n
    while uncovered:
        candidates = [(costs[i] / len(sets[i] & uncovered), i)
                      for i in range(len(sets)) if sets[i] & uncovered]
        if not candidates:
            raise ValueError("uncoverable element")
        _, i = min(candidates)
        new = sets[i] & uncovered
        for x in new:
            charges[x] = costs[i] / len(new)
        picked.append(i)
        uncovered -= new
    return picked, charges


def exact_cover(n, sets, costs):
    full = (1 << n) - 1
    masks = [sum(1 << x for x in s) for s in sets]
    dp = [float("inf")] * (1 << n)
    dp[0] = 0.0
    for mask in range(1 << n):
        for sm, cost in zip(masks, costs):
            dp[mask | sm] = min(dp[mask | sm], dp[mask] + cost)
    return dp[full]


def self_test():
    rng = Random(1618033)
    for n in range(1, 11):
        harmonic = sum(1 / i for i in range(1, n + 1))
        for _ in range(80):
            sets = [{x} for x in range(n)]
            sets += [{x for x in range(n) if rng.random() < .4} for _ in range(n)]
            costs = [rng.randint(1, 12) for _ in sets]
            picked, charges = greedy_cover(n, sets, costs)
            alg = sum(costs[i] for i in picked)
            opt = exact_cover(n, sets, costs)
            assert abs(fsum(charges) - alg) < 1e-8
            assert alg <= harmonic * opt + 1e-8
    print("weighted greedy <= H_n * OPT on all oracle-checked instances")


if __name__ == "__main__":
    self_test()

# 动手改造：打印每轮 (集合、单位价、新覆盖元素、收费)。然后把评分改错为
# 最大新覆盖数，写一个带权反例让 `ALG <= H_n*OPT` 断言失败。
