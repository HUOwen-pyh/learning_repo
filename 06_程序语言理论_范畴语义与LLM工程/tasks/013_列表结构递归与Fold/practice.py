"""第013晚：用 foldr 解释列表构造子。"""
from collections.abc import Callable
from typing import TypeVar
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

A = TypeVar("A"); B = TypeVar("B")

def foldr(step: Callable[[A, B], B], base: B, xs: list[A]) -> B:
    result = base
    for value in reversed(xs): result = step(value, result)
    return result

def map_fold(fn: Callable[[A], B], xs: list[A]) -> list[B]:
    return foldr(lambda x, acc: [fn(x)] + acc, [], xs)

def append_fold(xs: list[A], ys: list[A]) -> list[A]:
    return foldr(lambda x, acc: [x] + acc, ys.copy(), xs)

def main() -> None:
    assert foldr(lambda x, y: x + y, 0, []) == 0            # 最小正例
    assert foldr(lambda x, y: x + y, 0, [1, 2, 3]) == 6
    assert map_fold(lambda x: 2 * x, [1, 2]) == [2, 4]
    assert append_fold([], [3]) == [3]
    assert append_fold([1, 2], [3]) == [1, 2, 3]
    assert foldr(lambda x, y: x - y, 0, [1, 2]) == -1       # 非结合反例
    print("通过：fold 的 base/step 分别解释 nil/cons。")

if __name__ == "__main__": main()

# 动手改造：实现 foldl，并找出 foldl 与 foldr 在减法上的最小差异输入。
