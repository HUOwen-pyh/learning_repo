"""自由幺半群 F ⊣ 遗忘函子 U：单位、余单位与两条三角恒等式。"""
from __future__ import annotations

from collections.abc import Callable, Iterable
from functools import reduce
import sys
from typing import TypeVar

sys.stdout.reconfigure(encoding="utf-8")

X = TypeVar("X")
M = TypeVar("M")
Word = tuple[X, ...]


def eta(x: X) -> Word[X]:
    """η_X : X → U(FX)，把生成元送到单字词。"""
    return (x,)


def free_map(f: Callable[[X], M], word: Word[X]) -> Word[M]:
    """F(f) 逐字映射。"""
    return tuple(map(f, word))


def epsilon(words: Iterable[M], op: Callable[[M, M], M], identity: M) -> M:
    """ε_M : F(U(M)) → M，按 M 的幺半群运算求值。"""
    return reduce(op, words, identity)


def left_triangle(word: Word[X]) -> bool:
    # F X --Fη--> F U F X --ε_FX--> F X
    nested: Word[Word[X]] = free_map(eta, word)
    return epsilon(nested, lambda a, b: a + b, ()) == word


def right_triangle(value: int) -> bool:
    # U M --η_UM--> U F U M --Uε_M--> U M，取 M=(Z,+,0)。
    return epsilon(eta(value), lambda a, b: a + b, 0) == value


def main() -> None:
    for word in [(), ("a",), ("a", "b", "a")]:
        assert left_triangle(word)
    for value in [-3, 0, 7]:
        assert right_triangle(value)

    nested = (("a",), ("b",), ("c",))
    correct = epsilon(nested, lambda a, b: a + b, ())
    bad_epsilon = tuple(reversed(correct))
    assert correct == ("a", "b", "c")
    assert bad_epsilon != correct  # 逆序“余单位”破坏第一三角律。
    assert epsilon((), lambda a, b: a + b, 0) == 0  # 空词边界。
    print("自由幺半群伴随的两条三角恒等式与坏余单位反例通过")


if __name__ == "__main__":
    main()

# 动手改造：把整数加法换成字符串连接，并验证 ε 仍是幺半群同态。
