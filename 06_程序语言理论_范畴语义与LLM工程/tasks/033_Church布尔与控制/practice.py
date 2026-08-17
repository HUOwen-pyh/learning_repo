"""第 033 晚：Church boolean 是二选一的函数。"""
from __future__ import annotations
import sys
from typing import Callable, TypeVar

sys.stdout.reconfigure(encoding="utf-8")
T = TypeVar("T")
Thunk = Callable[[], T]
ChurchBool = Callable[[Thunk[T]], Callable[[Thunk[T]], T]]

TRUE: ChurchBool = lambda yes: lambda no: yes()
FALSE: ChurchBool = lambda yes: lambda no: no()

def choose(b: ChurchBool, yes: Thunk[T], no: Thunk[T]) -> T:
    return b(yes)(no)

def decode(b: ChurchBool) -> bool:
    out = choose(b, lambda: "T", lambda: "F")
    if out not in {"T", "F"}: raise ValueError("不是 Church 布尔行为")
    return out == "T"

touched: list[str] = []
assert choose(TRUE, lambda: "yes", lambda: touched.append("bad")) == "yes"  # 正例/惰性
assert decode(FALSE) is False                                                # 边界
try:
    decode(lambda yes: lambda no: "maybe")                                  # 反例
    raise AssertionError("应拒绝非法编码")
except ValueError:
    pass
assert touched == []

# 动手改造：只用函数应用定义 NOT/AND/OR，并为每个真值表写断言。
print("033 通过：Church 布尔按行为选择分支，未执行未选 thunk。")

