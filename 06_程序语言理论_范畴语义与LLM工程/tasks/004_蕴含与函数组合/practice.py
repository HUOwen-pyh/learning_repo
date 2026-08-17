"""第004晚：以函数组合实现蕴含传递。"""
from typing import Callable, TypeVar
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

A = TypeVar("A")
B = TypeVar("B")
C = TypeVar("C")

def compose(g: Callable[[B], C], f: Callable[[A], B]) -> Callable[[A], C]:
    return lambda value: g(f(value))

def extensionally_equal(f: Callable[[A], object], g: Callable[[A], object],
                        samples: tuple[A, ...]) -> bool:
    return all(f(x) == g(x) for x in samples)

def main() -> None:
    inc = lambda x: x + 1
    double = lambda x: 2 * x
    show = lambda x: f"[{x}]"
    assert compose(double, inc)(3) == 8                 # 最小正例
    assert compose(inc, double)(3) == 7                 # 次序反例
    left = compose(show, compose(double, inc))
    right = compose(compose(show, double), inc)
    assert extensionally_equal(left, right, (-2, 0, 5))
    assert compose(str.upper, lambda s: s)("") == ""   # 边界输入
    print("通过：蕴含传递对应函数组合；样本相等不等于一般证明。")

if __name__ == "__main__":
    main()

# 动手改造：实现 curry/uncurry，并在有限样本上验证两个往返律。
