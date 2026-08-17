"""第 028 晚：de Bruijn shift/substitution/beta。"""
from __future__ import annotations

import sys
from dataclasses import dataclass

sys.stdout.reconfigure(encoding="utf-8")


@dataclass(frozen=True)
class V: index: int
@dataclass(frozen=True)
class L: body: "Term"
@dataclass(frozen=True)
class A: fn: "Term"; arg: "Term"
Term = V | L | A


def shift(delta: int, cutoff: int, t: Term) -> Term:
    if isinstance(t, V):
        new = t.index + delta if t.index >= cutoff else t.index
        if new < 0:
            raise ValueError("移位产生负索引")
        return V(new)
    if isinstance(t, L):
        return L(shift(delta, cutoff + 1, t.body))
    return A(shift(delta, cutoff, t.fn), shift(delta, cutoff, t.arg))


def subst(index: int, replacement: Term, t: Term, depth: int = 0) -> Term:
    if isinstance(t, V):
        return shift(depth, 0, replacement) if t.index == index + depth else t
    if isinstance(t, L):
        return L(subst(index, replacement, t.body, depth + 1))
    return A(subst(index, replacement, t.fn, depth), subst(index, replacement, t.arg, depth))


def beta(t: Term) -> Term | None:
    if not (isinstance(t, A) and isinstance(t.fn, L)):
        return None
    lifted = shift(1, 0, t.arg)
    replaced = subst(0, lifted, t.fn.body)
    return shift(-1, 0, replaced)


assert beta(A(L(V(0)), V(0))) == V(0)                         # 正例
assert beta(V(0)) is None                                     # 反例：不是 redex
nested = L(A(V(1), V(0)))
assert shift(1, 0, nested) == L(A(V(2), V(0)))                # 边界：局部 #0 不移

# 动手改造：实现 normal_order_step，能在 fn/body/arg 中寻找最左最外 redex。
print("028 通过：移位与替换保持了嵌套 binder 的索引关系。")

