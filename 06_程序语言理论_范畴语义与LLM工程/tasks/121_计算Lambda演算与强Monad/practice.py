"""State Monad 的 tensorial strength 及其 η/μ 相容实例。"""
from __future__ import annotations

import sys
from collections.abc import Callable
from typing import TypeVar

sys.stdout.reconfigure(encoding="utf-8")

A = TypeVar("A")
B = TypeVar("B")
State = Callable[[int], tuple[A, int]]


def pure(value: A) -> State[A]:
    return lambda state: (value, state)


def fmap(function: Callable[[A], B], computation: State[A]) -> State[B]:
    def run(state: int) -> tuple[B, int]:
        value, next_state = computation(state)
        return function(value), next_state

    return run


def join(nested: State[State[A]]) -> State[A]:
    def run(state: int) -> tuple[A, int]:
        inner, next_state = nested(state)
        return inner(next_state)

    return run


def strength(environment: A, computation: State[B]) -> State[tuple[A, B]]:
    def run(state: int) -> tuple[tuple[A, B], int]:
        value, next_state = computation(state)
        return (environment, value), next_state

    return run


def main() -> None:
    calls: list[int] = []

    def tick(state: int) -> tuple[int, int]:
        calls.append(state)
        return state * 2, state + 1

    assert strength("meta", tick)(3) == (("meta", 6), 4)
    assert calls == [3], "strength 不得重复运行 effectful computation"

    # (id × η); t = η：给纯值加环境，不得改变状态。
    assert strength("env", pure(9))(5) == pure(("env", 9))(5)

    # (id × μ);t = t;T(t);μ 的 State 有限实例。
    nested: State[State[int]] = lambda state: (
        lambda inner_state: (state + inner_state, inner_state + 10),
        state + 1,
    )
    left = strength("env", join(nested))(2)
    right = join(fmap(lambda pair: strength(pair[0], pair[1]), strength("env", nested)))(2)
    assert left == right == (("env", 5), 13)
    print("State strength 的单次执行、η 与 μ 相容实例通过")


if __name__ == "__main__":
    main()

# 动手改造：实现右 strength TB×A→T(B×A)，检查与 swap 的相容性。
