"""第 030 晚：最左最外 beta 一步与有界轨迹。"""
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

def step(t: Term) -> Term | None:
    if isinstance(t, App) and isinstance(t.fn, Lam):
        return subst(t.fn.body, t.fn.param, t.arg)
    if isinstance(t, App):
        left = step(t.fn)
        if left is not None: return App(left, t.arg)
        right = step(t.arg)
        return App(t.fn, right) if right is not None else None
    if isinstance(t, Lam):
        body = step(t.body)
        return Lam(t.param, body) if body is not None else None
    return None

def trace(t: Term, gas: int) -> list[Term]:
    out = [t]
    for _ in range(gas):
        nxt = step(out[-1])
        if nxt is None: break
        out.append(nxt)
    return out

i = Lam("x", Var("x"))
assert step(App(i, Lam("y", Var("y")))) == Lam("y", Var("y"))  # 正例
assert step(Var("z")) is None                                  # 反例
assert trace(i, 0) == [i]                                      # 边界：零步闭包
capture_case = step(App(Lam("x", Lam("y", Var("x"))), Var("y")))
assert isinstance(capture_case, Lam) and capture_case.param != "y"
assert free_vars(capture_case) == {"y"}                       # 自由 y 不得被捕获

# 动手改造：返回 (rule, next_term)，并验证每条轨迹的 rule 标签与 AST 位置一致。
print("030 通过：β 一步已组合成包含零步的可回放轨迹。")
