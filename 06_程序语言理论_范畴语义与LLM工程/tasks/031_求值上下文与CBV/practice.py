"""第 031 晚：确定的左到右 CBV 小步求值。"""
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

def free_vars(t: Term) -> set[str]:
    if isinstance(t, Var): return {t.name}
    if isinstance(t, App): return free_vars(t.fn) | free_vars(t.arg)
    return free_vars(t.body) - {t.param}

def all_names(t: Term) -> set[str]:
    if isinstance(t, Var): return {t.name}
    if isinstance(t, App): return all_names(t.fn) | all_names(t.arg)
    return {t.param} | all_names(t.body)

def rename_bound(t: Term, old: str, new: str) -> Term:
    if isinstance(t, Var): return Var(new) if t.name == old else t
    if isinstance(t, App): return App(rename_bound(t.fn, old, new), rename_bound(t.arg, old, new))
    return t if t.param == old else Lam(t.param, rename_bound(t.body, old, new))

def subst(t: Term, x: str, s: Term) -> Term:
    if isinstance(t, Var): return s if t.name == x else t
    if isinstance(t, App): return App(subst(t.fn, x, s), subst(t.arg, x, s))
    if t.param == x: return t
    if t.param in free_vars(s):
        avoid = all_names(t.body) | free_vars(s) | {x}
        i = 0
        while (fresh := f"v{i}") in avoid: i += 1
        return Lam(fresh, subst(rename_bound(t.body, t.param, fresh), x, s))
    return Lam(t.param, subst(t.body, x, s))

def step_cbv(t: Term) -> Term | None:
    if not isinstance(t, App): return None
    if not isinstance(t.fn, Lam):
        fn2 = step_cbv(t.fn)
        return App(fn2, t.arg) if fn2 is not None else None
    if not isinstance(t.arg, Lam):
        arg2 = step_cbv(t.arg)
        return App(t.fn, arg2) if arg2 is not None else None
    return subst(t.fn.body, t.fn.param, t.arg)

i, k = Lam("x", Var("x")), Lam("x", Lam("y", Var("x")))
term = App(i, App(i, k))
assert step_cbv(term) == App(i, k)                              # 正例：先实参
assert step_cbv(App(i, Var("free"))) is None                   # 反例：开放项 stuck
assert step_cbv(i) is None                                     # 边界：值

# 动手改造：实现上下文类 Hole/FnCtx/ArgCtx，再证明 plug(*decompose(t)) == t。
print("031 通过：CBV 的唯一求值位置已由规则确定。")
