"""第 029 晚：判定 lambda 值、redex 与 beta 正规形。"""
from __future__ import annotations
import sys
from dataclasses import dataclass

sys.stdout.reconfigure(encoding="utf-8")

@dataclass(frozen=True)
class Var: name: str
@dataclass(frozen=True)
class Lam: param: str; body: "Term"
@dataclass(frozen=True)
class App: fn: "Term"; arg: "Term"
Term = Var | Lam | App

def is_value(t: Term) -> bool:
    return isinstance(t, Lam)

def is_beta_normal(t: Term) -> bool:
    if isinstance(t, Var):
        return True
    if isinstance(t, Lam):
        return is_beta_normal(t.body)
    if isinstance(t.fn, Lam):
        return False
    return is_beta_normal(t.fn) and is_beta_normal(t.arg)

closed_value_with_redex = Lam("x", App(Lam("y", Var("y")), Var("x")))
assert is_value(closed_value_with_redex)                       # 正例：CBV value
assert not is_beta_normal(closed_value_with_redex)             # 反例：不是 full normal
neutral = App(Var("f"), Lam("x", Var("x")))
assert not is_value(neutral) and is_beta_normal(neutral)       # 边界：开放 neutral

# 动手改造：加入 is_whnf，并找出同时满足 WHNF 但不满足 beta-normal 的两种形状。
print("029 通过：值与 β 正规形已按不同停机判据区分。")

