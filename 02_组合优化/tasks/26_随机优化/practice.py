"""第 26 晚：报童 SAA、独立真实分布评价与 replication 区间。"""
from __future__ import annotations
import sys
sys.stdout.reconfigure(encoding="utf-8", errors="backslashreplace")

from collections import Counter
import math
import random
import statistics

SCENARIOS = [(4, 0.10), (7, 0.20), (10, 0.40), (13, 0.20), (16, 0.10)]
PURCHASE, HOLDING, SHORTAGE = 2.0, 1.0, 5.0
Q_RANGE = range(0, 21)


def scenario_cost(q: int, demand: int) -> float:
    return PURCHASE * q + HOLDING * max(q - demand, 0) + SHORTAGE * max(demand - q, 0)


def true_cost(q: int) -> float:
    assert math.isclose(sum(p for _, p in SCENARIOS), 1.0)
    return sum(prob * scenario_cost(q, demand) for demand, prob in SCENARIOS)


def saa_choice(sample: list[int]) -> int:
    return min(
        Q_RANGE,
        key=lambda q: (sum(scenario_cost(q, d) for d in sample) / len(sample), q),
    )


def draw_sample(rng: random.Random, n: int) -> list[int]:
    demands, probs = zip(*SCENARIOS)
    return rng.choices(demands, weights=probs, k=n)


def experiment(sample_size: int, replications: int, seed: int) -> tuple[float, float, Counter[int]]:
    rng = random.Random(seed)
    optimum = min(true_cost(q) for q in Q_RANGE)
    choices, regrets = [], []
    for _ in range(replications):
        q = saa_choice(draw_sample(rng, sample_size))
        choices.append(q)
        regrets.append(true_cost(q) - optimum)
    mean = statistics.mean(regrets)
    half_width = 1.96 * statistics.stdev(regrets) / math.sqrt(replications)
    return mean, half_width, Counter(choices)


def main() -> None:
    true_q = min(Q_RANGE, key=true_cost)
    true_optimum = true_cost(true_q)
    small = experiment(12, 200, seed=101)
    large = experiment(200, 200, seed=202)
    assert true_q == 10
    assert all(true_cost(q) >= true_optimum - 1e-12 for q in Q_RANGE)
    assert large[0] <= small[0]  # 固定种子下，大样本平均 regret 更低。
    print("true optimum q =", true_q, "expected cost =", round(true_optimum, 3))
    print("N=12 mean regret/95% half-width =", round(small[0], 4), round(small[1], 4))
    print("N=12 decisions =", sorted(small[2].items()))
    print("N=200 mean regret/95% half-width =", round(large[0], 4), round(large[1], 4))
    print("N=200 decisions =", sorted(large[2].items()))


if __name__ == "__main__":
    main()

# 动手改造：
# 1. 用独立的大验证样本代替已知真实分布，并同时报告验证误差。
# 2. 加入 CVaR_0.9 目标，比较期望最优与尾部风险最优 q。
