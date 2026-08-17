"""第 034 晚：Church numeral、加法和乘法。"""
from __future__ import annotations
import sys
from typing import Callable, TypeVar

sys.stdout.reconfigure(encoding="utf-8")
T = TypeVar("T")
Church = Callable[[Callable[[T], T]], Callable[[T], T]]

def church(n: int) -> Church:
    if n < 0: raise ValueError("Church 自然数不能为负")
    return lambda f: lambda x: _repeat(f, x, n)

def _repeat(f, x, n: int):
    for _ in range(n): x = f(x)
    return x

def decode(n: Church) -> int:
    value = n(lambda x: x + 1)(0)
    trace = n(lambda xs: xs + ("step",))(())
    if type(value) is not int or value < 0 or not isinstance(trace, tuple) or len(trace) != value:
        raise ValueError("有限行为检查未通过：不是一致的 Church 迭代器")
    return value

def plus(m: Church, n: Church) -> Church:
    return lambda f: lambda x: m(f)(n(f)(x))

def mul(m: Church, n: Church) -> Church:
    return lambda f: m(n(f))

assert decode(plus(church(2), church(3))) == 5                 # 正例
assert decode(mul(church(2), church(3))) == 6
assert decode(church(0)) == 0                                 # 边界
try: church(-1)                                               # 反例
except ValueError: pass
else: raise AssertionError("应拒绝负数")
try: decode(lambda f: lambda x: 7)                            # 反例：只伪造 int 观察
except ValueError: pass
else: raise AssertionError("应拒绝不按 f 迭代的伪编码")

# 动手改造：实现 successor，并用计数包装器核对 church(n) 恰调用 f 共 n 次。
print("034 通过：自然数已表现为高阶函数的迭代次数。")
