"""第 27 晚：Gamma-budget 不确定下的鲁棒项目选择。"""
from __future__ import annotations
import sys
sys.stdout.reconfigure(encoding="utf-8", errors="backslashreplace")

from itertools import combinations
import random

NOMINAL = (20, 19, 17, 16, 15, 13, 12)
DEVIATION = (9, 2, 3, 2, 1, 1, 0)
CHOOSE = 3


def worst_value(chosen: tuple[int, ...], gamma: float) -> float:
    deviations = sorted((DEVIATION[i] for i in chosen), reverse=True)
    budget = min(gamma, float(len(deviations)))
    whole = int(budget)
    loss = sum(deviations[:whole])
    if whole < len(deviations):
        loss += (budget - whole) * deviations[whole]
    return float(sum(NOMINAL[i] for i in chosen) - loss)


def adversary_enumeration(chosen: tuple[int, ...], gamma: int) -> float:
    # 整数 Gamma：对手攻击至多 gamma 个已选项目。
    max_loss = max(
        sum(DEVIATION[i] for i in attacked)
        for r in range(min(gamma, len(chosen)) + 1)
        for attacked in combinations(chosen, r)
    )
    return float(sum(NOMINAL[i] for i in chosen) - max_loss)


def robust_optimum(gamma: float) -> tuple[float, tuple[int, ...]]:
    return max(
        (worst_value(chosen, gamma), chosen)
        for chosen in combinations(range(len(NOMINAL)), CHOOSE)
    )


def stress_mean(chosen: tuple[int, ...], seed: int = 9) -> float:
    rng = random.Random(seed)
    outcomes = [
        sum(NOMINAL[i] - rng.random() * DEVIATION[i] for i in chosen)
        for _ in range(2000)
    ]
    return sum(outcomes) / len(outcomes)


def main() -> None:
    gammas = (0.0, 1.0, 1.5, 2.0, 3.0)
    results = [(gamma, *robust_optimum(gamma)) for gamma in gammas]
    robust_values = [row[1] for row in results]
    assert all(a >= b for a, b in zip(robust_values, robust_values[1:]))
    for gamma in (0, 1, 2, 3):
        value, chosen = robust_optimum(float(gamma))
        assert value == adversary_enumeration(chosen, gamma)
    nominal_choice = robust_optimum(0.0)[1]
    robust_choice = robust_optimum(1.0)[1]
    assert worst_value(robust_choice, 1.0) >= worst_value(nominal_choice, 1.0)
    for gamma, value, chosen in results:
        print("Gamma =", gamma, "choice =", chosen, "nominal =", sum(NOMINAL[i] for i in chosen),
              "worst =", value)
    print("stress mean nominal/robust choices =", round(stress_mean(nominal_choice), 3),
          round(stress_mean(robust_choice), 3))


if __name__ == "__main__":
    main()

# 动手改造：
# 1. 加入项目类别上限（partition matroid），重新枚举 robustness frontier。
# 2. 用历史扰动分位数校准 deviation，并说明 Gamma 的业务解释。
