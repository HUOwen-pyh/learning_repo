"""第 10 晚：用有理数枚举二维 LP 顶点与活跃约束。"""
from __future__ import annotations
import sys
sys.stdout.reconfigure(encoding="utf-8", errors="backslashreplace")

from dataclasses import dataclass
from fractions import Fraction
import random


@dataclass(frozen=True)
class Constraint:
    a: Fraction
    b: Fraction
    rhs: Fraction
    name: str


Point = tuple[Fraction, Fraction]


def intersection(p: Constraint, q: Constraint) -> Point | None:
    det = p.a * q.b - q.a * p.b
    if det == 0:
        return None
    x = (p.rhs * q.b - q.rhs * p.b) / det
    y = (p.a * q.rhs - q.a * p.rhs) / det
    return x, y


def feasible(point: Point, constraints: list[Constraint]) -> bool:
    x, y = point
    return all(c.a * x + c.b * y <= c.rhs for c in constraints)


def vertices(constraints: list[Constraint]) -> list[Point]:
    found: set[Point] = set()
    for i, p in enumerate(constraints):
        for q in constraints[i + 1:]:
            point = intersection(p, q)
            if point is not None and feasible(point, constraints):
                found.add(point)
    return sorted(found)


def active(point: Point, constraints: list[Constraint]) -> list[str]:
    x, y = point
    return [c.name for c in constraints if c.a * x + c.b * y == c.rhs]


def maximize(points: list[Point], c: tuple[int, int]) -> tuple[Fraction, Point]:
    return max((c[0] * x + c[1] * y, (x, y)) for x, y in points)


def main() -> None:
    F = Fraction
    cons = [
        Constraint(F(1), F(1), F(4), "x+y<=4"),
        Constraint(F(2), F(1), F(5), "2x+y<=5"),
        Constraint(F(1), F(0), F(5, 2), "x<=2.5"),
        Constraint(F(-1), F(0), F(0), "x>=0"),
        Constraint(F(0), F(-1), F(0), "y>=0"),
    ]
    points = vertices(cons)
    value, best = maximize(points, (3, 2))
    assert feasible(best, cons) and value == 9 and best == (F(1), F(3))
    assert len(active(best, cons)) >= 2
    rng = random.Random(7)
    support = {}
    for _ in range(5):
        direction = (rng.randint(-3, 4), rng.randint(-3, 4))
        support[direction] = maximize(points, direction)[1]
    print("vertices =", [(float(x), float(y)) for x, y in points])
    print("max 3x+2y =", value, "at", best, "active =", active(best, cons))
    print("support vertices =", support)


if __name__ == "__main__":
    main()

# 动手改造：
# 1. 把目标改为 (1,1)，检测整条 x+y=4 是否多重最优。
# 2. 添加近乎平行的浮点约束，对比 Fraction 与 float 的结果。
