"""第 022 晚：把 lambda 项文法实现为归纳 AST。"""
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


def size(term: Term) -> int:
    if isinstance(term, Var):
        return 1
    if isinstance(term, Lam):
        return 1 + size(term.body)
    if isinstance(term, App):
        return 1 + size(term.fn) + size(term.arg)
    raise TypeError(f"未知 AST 节点: {term!r}")


def depth(term: Term) -> int:
    if isinstance(term, Var):
        return 1
    if isinstance(term, Lam):
        return 1 + depth(term.body)
    if isinstance(term, App):
        return 1 + max(depth(term.fn), depth(term.arg))
    raise TypeError("非法节点")


x = Var("x")                              # 边界：最小 AST
identity = Lam("x", x)                    # 正例
applied = App(identity, Var("y"))
assert size(x) == 1 and depth(x) == 1
assert size(applied) == 4 and depth(applied) == 3
try:                                      # 反例：文法之外的节点
    size(42)  # type: ignore[arg-type]
    raise AssertionError("应拒绝非法节点")
except TypeError:
    pass

# 动手改造：新增 Let(name, value, body)，同步补齐 size/depth，并写一个漏分支会失败的测试。
print("022 通过：BNF 已落实为可结构递归的 AST。")

