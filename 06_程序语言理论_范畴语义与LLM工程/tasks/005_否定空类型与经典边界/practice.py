"""第005晚：在有限域中检查“反驳器”，观察否定的方向。"""
from collections.abc import Callable, Iterable
from typing import Never
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

def is_refutation(predicate: Callable[[int], bool],
                  domain: Iterable[int]) -> tuple[bool, int | None]:
    """返回是否无正例；若失败，同时给出反例见证。"""
    for value in domain:
        if predicate(value):
            return False, value
    return True, None

def double_negation_intro(witness: int) -> Callable[[Callable[[int], Never]], Never]:
    """A→¬¬A：把 A 的见证交给任意 A→⊥ 的反驳器。"""
    return lambda refuter: refuter(witness)


class BottomReached(Exception):
    """运行时只用异常模拟无返回的 ⊥；它不是 ⊥ 的居民。"""

def main() -> None:
    impossible = lambda x: x < 0 and x >= 0
    ok, witness = is_refutation(impossible, range(-3, 4))
    assert ok and witness is None                         # 最小正例
    even = lambda x: x % 2 == 0
    ok, witness = is_refutation(even, range(3))
    assert not ok and witness == 0                        # 最小反例
    assert is_refutation(even, ())[0]                     # 空域边界
    def alleged_refuter(value: int) -> Never:
        raise BottomReached(f"refuter 被迫消费见证 {value}")
    try:
        double_negation_intro(2)(alleged_refuter)
    except BottomReached as error:
        assert "2" in str(error)
    else:
        raise AssertionError("A→¬¬A 没有把见证交给反驳器")
    print("通过：找到正例会击破否定；有限搜索无反例不等于一般定理。")

if __name__ == "__main__":
    main()

# 动手改造：让检查器返回全部最小反例，并区分 UNKNOWN 与已证明的否定。
