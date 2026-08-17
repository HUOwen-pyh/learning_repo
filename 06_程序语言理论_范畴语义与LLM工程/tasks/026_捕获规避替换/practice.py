"""第 026 晚：带新鲜名生成的捕获规避替换。"""
from __future__ import annotations

import sys
from dataclasses import dataclass

sys.stdout.reconfigure(encoding="utf-8")


@dataclass(frozen=True)
class Var:
    name: str


@dataclass(frozen=True)
class Lam:
    param: str
    body: "Term"


@dataclass(frozen=True)
class App:
    fn: "Term"
    arg: "Term"


Term = Var | Lam | App


def free_vars(t: Term) -> set[str]:
    if isinstance(t, Var):
        return {t.name}
    if isinstance(t, App):
        return free_vars(t.fn) | free_vars(t.arg)
    return free_vars(t.body) - {t.param}


def all_names(t: Term) -> set[str]:
    if isinstance(t, Var):
        return {t.name}
    if isinstance(t, App):
        return all_names(t.fn) | all_names(t.arg)
    return {t.param} | all_names(t.body)


def fresh(avoid: set[str], base: str = "v") -> str:
    i = 0
    while f"{base}{i}" in avoid:
        i += 1
    return f"{base}{i}"


def rename_bound(t: Term, old: str, new: str) -> Term:
    """调用方传入 binder 的 body；遇到同名内层 binder 时停止。"""
    if isinstance(t, Var):
        return Var(new) if t.name == old else t
    if isinstance(t, App):
        return App(rename_bound(t.fn, old, new), rename_bound(t.arg, old, new))
    if t.param == old:
        return t
    return Lam(t.param, rename_bound(t.body, old, new))


def subst(t: Term, name: str, replacement: Term) -> Term:
    if isinstance(t, Var):
        return replacement if t.name == name else t
    if isinstance(t, App):
        return App(subst(t.fn, name, replacement), subst(t.arg, name, replacement))
    if t.param == name:
        return t
    if t.param in free_vars(replacement):
        z = fresh(all_names(t.body) | free_vars(replacement) | {name}, t.param)
        renamed = rename_bound(t.body, t.param, z)
        return Lam(z, subst(renamed, name, replacement))
    return Lam(t.param, subst(t.body, name, replacement))


assert subst(App(Var("x"), Var("z")), "x", Var("y")) == App(Var("y"), Var("z"))
shadowed = Lam("x", Var("x"))
assert subst(shadowed, "x", Var("y")) == shadowed              # 反例：不能穿过 binder
capturable = subst(Lam("y", Var("x")), "x", Var("y"))
assert isinstance(capturable, Lam) and capturable.param != "y" # 边界：必须改名
assert free_vars(capturable) == {"y"}
inner_binder = Lam("y", Lam("y0", Var("y")))
renamed = subst(inner_binder, "x", Var("y"))
assert isinstance(renamed, Lam) and renamed.param not in {"y", "y0"}
assert free_vars(renamed) == set()  # 外层 y 的出现不能被内层 y0 捕获。

# 动手改造：让 fresh 使用确定性全局候选序列，并测试输入中已有 y0、y1 的情况。
print("026 通过：替换保留了替入项的自由变量，未发生捕获。")
