"""第 032 晚：用 K I Omega 比较 CBN 与 CBV。"""
from __future__ import annotations
import sys
from dataclasses import dataclass

sys.stdout.reconfigure(encoding="utf-8")

@dataclass(frozen=True)
class V: name: str
@dataclass(frozen=True)
class L: param: str; body: "T"
@dataclass(frozen=True)
class A: fn: "T"; arg: "T"
T = V | L | A

def free_vars(t: T) -> set[str]:
    if isinstance(t, V): return {t.name}
    if isinstance(t, A): return free_vars(t.fn) | free_vars(t.arg)
    return free_vars(t.body) - {t.param}

def all_names(t: T) -> set[str]:
    if isinstance(t, V): return {t.name}
    if isinstance(t, A): return all_names(t.fn) | all_names(t.arg)
    return {t.param} | all_names(t.body)

def rename_bound(t: T, old: str, new: str) -> T:
    if isinstance(t, V): return V(new) if t.name == old else t
    if isinstance(t, A): return A(rename_bound(t.fn, old, new), rename_bound(t.arg, old, new))
    return t if t.param == old else L(t.param, rename_bound(t.body, old, new))

def sub(t: T, x: str, s: T) -> T:
    if isinstance(t, V): return s if t.name == x else t
    if isinstance(t, A): return A(sub(t.fn, x, s), sub(t.arg, x, s))
    if t.param == x: return t
    if t.param in free_vars(s):
        avoid = all_names(t.body) | free_vars(s) | {x}
        i = 0
        while (fresh := f"v{i}") in avoid: i += 1
        return L(fresh, sub(rename_bound(t.body, t.param, fresh), x, s))
    return L(t.param, sub(t.body, x, s))

def cbn(t: T) -> T | None:
    if isinstance(t, A) and isinstance(t.fn, L): return sub(t.fn.body, t.fn.param, t.arg)
    if isinstance(t, A):
        fn = cbn(t.fn)
        return A(fn, t.arg) if fn is not None else None
    return None

def cbv(t: T) -> T | None:
    if not isinstance(t, A): return None
    if not isinstance(t.fn, L):
        fn = cbv(t.fn); return A(fn, t.arg) if fn is not None else None
    if not isinstance(t.arg, L):
        arg = cbv(t.arg); return A(t.fn, arg) if arg is not None else None
    return sub(t.fn.body, t.fn.param, t.arg)

def run(t: T, strategy, gas: int) -> tuple[T, bool]:
    for _ in range(gas):
        nxt = strategy(t)
        if nxt is None: return t, True
        t = nxt
    return t, False

i = L("z", V("z")); k = L("x", L("y", V("x")))
w = L("w", A(V("w"), V("w"))); omega = A(w, w)
target = A(A(k, i), omega)
assert run(target, cbn, 5) == (i, True)                         # 正例
assert run(target, cbv, 8)[1] is False                         # 反例：预算耗尽
assert run(i, cbv, 0) == (i, False)                            # PLFA 约定：零 gas 不检查

# 动手改造：为 run 增加步数和策略名，输出可比较的结构化实验记录。
print("032 通过：CBN 跳过未用 Ω，CBV 在给定预算内未结束。")
