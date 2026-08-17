"""含 Print effect 的常量折叠与值/trace 语义差分。"""
from __future__ import annotations

import random
import sys
from dataclasses import dataclass

sys.stdout.reconfigure(encoding="utf-8")


@dataclass(frozen=True)
class N:
    value: int


@dataclass(frozen=True)
class Add:
    left: object
    right: object


@dataclass(frozen=True)
class Mul:
    left: object
    right: object


@dataclass(frozen=True)
class Print:
    value: object
    body: object


def evaluate(term: object, trace: list[int] | None = None) -> tuple[int, tuple[int, ...]]:
    output = [] if trace is None else trace

    def go(node: object) -> int:
        if isinstance(node, N):
            return node.value
        if isinstance(node, Add):
            return go(node.left) + go(node.right)
        if isinstance(node, Mul):
            return go(node.left) * go(node.right)
        if isinstance(node, Print):
            output.append(go(node.value))
            return go(node.body)
        raise TypeError(node)

    return go(term), tuple(output)


def fold(term: object) -> object:
    if isinstance(term, N):
        return term
    if isinstance(term, Print):
        return Print(fold(term.value), fold(term.body))  # 保留可观察 effect。
    if isinstance(term, (Add, Mul)):
        left, right = fold(term.left), fold(term.right)
        if isinstance(left, N) and isinstance(right, N):
            result = left.value + right.value if isinstance(term, Add) else left.value * right.value
            return N(result)
        return type(term)(left, right)
    raise TypeError(term)


def mutant_fold(term: object) -> object:
    """错误规则 x*0→0：没有确认 x 为纯，因而可能删除 Print。"""
    if isinstance(term, Mul) and isinstance(term.right, N) and term.right.value == 0:
        return N(0)
    if isinstance(term, (Add, Mul)):
        return type(term)(mutant_fold(term.left), mutant_fold(term.right))
    if isinstance(term, Print):
        return Print(mutant_fold(term.value), mutant_fold(term.body))
    return term


def generate(rng: random.Random, depth: int) -> object:
    if depth == 0:
        return N(rng.randrange(10))
    constructor = rng.choice((Add, Mul))
    return constructor(generate(rng, depth - 1), generate(rng, depth - 1))


def main() -> None:
    rng = random.Random(146)
    for _ in range(200):
        term = generate(rng, 4)
        assert evaluate(fold(term)) == evaluate(term)

    effectful = Mul(Print(N(7), Add(N(2), N(2))), N(0))
    assert evaluate(fold(effectful)) == (0, (7,))
    original = evaluate(effectful)
    mutated = evaluate(mutant_fold(effectful))
    assert original[0] == mutated[0] == 0
    assert original[1] == (7,) and mutated[1] == (), "mutant 必须被 trace 差异击穿"
    print("200 个差分与 Print effect mutant 反例通过")


if __name__ == "__main__":
    main()

# 动手改造：给 effect 注记加纯度分析，仅在证明 x 纯时允许 x*0→0。
