"""第 035 晚：eager Z 组合子与安全的 gas 状态。"""
from __future__ import annotations
import sys
from dataclasses import dataclass
from typing import Callable

sys.stdout.reconfigure(encoding="utf-8")

def Z(f):
    return (lambda x: f(lambda *args: x(x)(*args)))(lambda x: f(lambda *args: x(x)(*args)))

factorial = Z(lambda rec: lambda n: 1 if n == 0 else n * rec(n - 1))
assert factorial(5) == 120                                    # 正例
assert factorial(0) == 1                                      # 边界

@dataclass(frozen=True)
class Done: value: str; steps: int
@dataclass(frozen=True)
class OutOfGas: current: str; steps: int

def run(step: Callable[[str], str | None], state: str, gas: int) -> Done | OutOfGas:
    if gas < 0:
        raise ValueError("gas 必须是自然数")
    for used in range(gas):
        nxt = step(state)
        if nxt is None: return Done(state, used)
        state = nxt
    return OutOfGas(state, gas)  # 不额外偷跑第 gas+1 次 step。

omega_step = lambda state: state if state == "Ω" else None
assert run(omega_step, "Ω", 8) == OutOfGas("Ω", 8)             # 反例：自循环
assert run(omega_step, "value", 1) == Done("value", 0)
assert run(omega_step, "value", 0) == OutOfGas("value", 0)    # PLFA 的零 gas 边界

# 动手改造：加入 Cycle 状态；说明检测到重复状态何时足以证明确定系统不终止。
print("035 通过：递归可由不动点表达，发散候选由 gas 安全隔离。")
