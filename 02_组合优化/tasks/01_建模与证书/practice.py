"""第 01 晚：0-1 项目组合模型、独立检查器与界。Python 3.11+。"""
from __future__ import annotations
import sys
sys.stdout.reconfigure(encoding="utf-8", errors="backslashreplace")

from dataclasses import dataclass
from itertools import product


@dataclass(frozen=True)
class Project:
    name: str
    cost: int
    value: int


PROJECTS = [
    Project("搜索", 5, 10),
    Project("支付", 6, 12),
    Project("推荐", 4, 9),
    Project("风控", 3, 6),
    Project("分析", 2, 4),
]
BUDGET = 12
# 若选推荐(2)，必须选搜索(0)；支付(1)与风控(3)互斥。


def feasible(bits: tuple[int, ...]) -> tuple[bool, list[str]]:
    errors: list[str] = []
    if len(bits) != len(PROJECTS) or any(x not in (0, 1) for x in bits):
        return False, ["变量必须是正确长度的 0-1 向量"]
    cost = sum(p.cost * x for p, x in zip(PROJECTS, bits))
    if cost > BUDGET:
        errors.append(f"预算超出：{cost}>{BUDGET}")
    if bits[2] > bits[0]:
        errors.append("推荐依赖搜索")
    if bits[1] + bits[3] > 1:
        errors.append("支付与风控互斥")
    return not errors, errors


def objective(bits: tuple[int, ...]) -> int:
    return sum(p.value * x for p, x in zip(PROJECTS, bits))


def exact_solve() -> tuple[int, tuple[int, ...], int]:
    best_value, best = -1, ()
    checked = 0
    for bits in product((0, 1), repeat=len(PROJECTS)):
        checked += 1
        ok, _ = feasible(bits)
        if ok and objective(bits) > best_value:
            best_value, best = objective(bits), bits
    return best_value, best, checked


def fractional_knapsack_upper_bound() -> float:
    """忽略逻辑约束并允许分数选择，得到最大化问题的可靠上界。"""
    remain, bound = BUDGET, 0.0
    for p in sorted(PROJECTS, key=lambda q: q.value / q.cost, reverse=True):
        take = min(1.0, remain / p.cost)
        bound += take * p.value
        remain -= int(take * p.cost) if take == 1.0 else remain
        if remain == 0:
            break
    return bound


def main() -> None:
    optimum, solution, checked = exact_solve()
    ok, errors = feasible(solution)  # 独立于搜索逻辑再次核验
    assert ok, errors
    assert objective(solution) == optimum
    assert not feasible((0, 1, 1, 0, 1))[0]  # 推荐缺少搜索
    assert not feasible((1, 1, 0, 1, 0))[0]  # 互斥
    upper = fractional_knapsack_upper_bound()
    assert upper + 1e-9 >= optimum
    chosen = [p.name for p, x in zip(PROJECTS, solution) if x]
    print(f"枚举 {checked} 个候选；最优价值={optimum}，方案={chosen}")
    print(f"分数背包松弛上界={upper:.2f}，绝对 gap={upper-optimum:.2f}")


if __name__ == "__main__":
    main()

# 动手改造：
# 1. 加入规则“分析与搜索不能同时选”，同步修改检查器并写拒绝用例。
# 2. 构造 value/cost 贪心严格劣于最优解的 3 项实例。
