"""第 025 晚：用 binder 距离得到 alpha 规范形。"""
from __future__ import annotations

import sys
from dataclasses import dataclass
from typing import TypeAlias

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


Term: TypeAlias = Var | Lam | App
Normal: TypeAlias = tuple


def alpha_normal(term: Term, binders: tuple[str, ...] = ()) -> Normal:
    if isinstance(term, Var):
        for distance, name in enumerate(reversed(binders)):
            if term.name == name:
                return ("bound", distance)
        return ("free", term.name)
    if isinstance(term, Lam):
        return ("lam", alpha_normal(term.body, binders + (term.param,)))
    if isinstance(term, App):
        return ("app", alpha_normal(term.fn, binders), alpha_normal(term.arg, binders))
    raise TypeError("非法项")


def alpha_eq(left: Term, right: Term) -> bool:
    return alpha_normal(left) == alpha_normal(right)


assert alpha_eq(Lam("x", Var("x")), Lam("y", Var("y")))       # 正例
assert not alpha_eq(Lam("x", Var("y")), Lam("y", Var("y")))  # 反例：自由/绑定
nested_a = Lam("x", Lam("x", Var("x")))
nested_b = Lam("a", Lam("b", Var("b")))
assert alpha_eq(nested_a, nested_b)                              # 边界：遮蔽

# 动手改造：加入 Let binder，并使 alpha_normal 正确处理 value 与 body 的不同作用域。
print("025 通过：α 等价已化为规范形的结构相等。")

