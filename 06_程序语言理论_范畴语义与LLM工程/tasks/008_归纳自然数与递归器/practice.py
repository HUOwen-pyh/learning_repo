"""第008晚：Peano 自然数及其结构递归器。"""
from dataclasses import dataclass
from typing import Callable, TypeVar
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

@dataclass(frozen=True)
class Zero: pass
@dataclass(frozen=True)
class Succ: pred: object

T = TypeVar("T")

def fold_nat(n: object, zero: T, step: Callable[[T], T]) -> T:
    if isinstance(n, Zero): return zero
    if isinstance(n, Succ): return step(fold_nat(n.pred, zero, step))
    raise TypeError("不是归纳自然数")

def from_int(n: int) -> object:
    if n < 0: raise ValueError("自然数不能为负")
    result: object = Zero()
    for _ in range(n): result = Succ(result)
    return result

def to_int(n: object) -> int:
    return fold_nat(n, 0, lambda x: x + 1)

def add(a: object, b: object) -> object:
    return fold_nat(a, b, Succ)

def main() -> None:
    assert to_int(Zero()) == 0                              # 最小正例
    assert to_int(Succ(Zero())) == 1
    assert to_int(add(from_int(2), from_int(3))) == 5
    try: from_int(-1)                                      # 最小反例
    except ValueError: pass
    else: raise AssertionError("负数被当作自然数")
    print("通过：递归严格沿 pred 下降，零与后继覆盖全部情况。")

if __name__ == "__main__": main()

# 动手改造：只用 fold_nat 定义乘法，并加入 0×n 与 1×n 测试。
