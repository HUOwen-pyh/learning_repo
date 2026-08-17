"""第003晚：带标签的和类型与穷尽分支。"""
from dataclasses import dataclass
from typing import Callable
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

@dataclass(frozen=True)
class Left:
    value: object

@dataclass(frozen=True)
class Right:
    value: object

def case(value: object, on_left: Callable[[object], object],
         on_right: Callable[[object], object]) -> object:
    if isinstance(value, Left):
        return on_left(value.value)
    if isinstance(value, Right):
        return on_right(value.value)
    raise TypeError("和值必须带 Left/Right 标签")

def swap(value: object) -> object:
    return case(value, Right, Left)

def main() -> None:
    assert case(Left(3), lambda x: x + 1, lambda x: 0) == 4  # 最小正例左
    assert case(Right("x"), len, lambda x: len(x) + 1) == 2  # 最小正例右
    for value in (Left(1), Right("err")):
        assert swap(swap(value)) == value
    try:
        case(42, str, str)                                  # 最小反例
    except TypeError:
        pass
    else:
        raise AssertionError("未标记的值被当成析取证据")
    print("通过：和值保留来源标签，消去必须覆盖左右分支。")

if __name__ == "__main__":
    main()

# 动手改造：实现 map_sum(f, g, value)，并验证恒等映射不改变值。
