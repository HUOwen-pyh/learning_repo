"""第 024 晚：自由变量、闭项与遮蔽。"""
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


def free_vars(term: Term) -> frozenset[str]:
    if isinstance(term, Var):
        return frozenset({term.name})
    if isinstance(term, App):
        return free_vars(term.fn) | free_vars(term.arg)
    if isinstance(term, Lam):
        return free_vars(term.body) - {term.param}
    raise TypeError("非法项")


def closed(term: Term) -> bool:
    return not free_vars(term)


identity = Lam("x", Var("x"))
open_term = Lam("x", App(Var("x"), Var("y")))
shadowed = Lam("x", App(Lam("x", Var("x")), Var("x")))
assert closed(identity)                                      # 正例
assert free_vars(open_term) == frozenset({"y"})             # 反例：并非闭项
assert closed(shadowed) and free_vars(shadowed) == frozenset()  # 边界：遮蔽

# 动手改造：返回每个 Var 出现所对应 binder 的 AST 路径；自由出现用 None。
print("024 通过：自由变量与遮蔽已按 AST 作用域计算。")

