"""第 037 晚：syntax-directed STLC 类型检查器。"""
from __future__ import annotations
import sys
from dataclasses import dataclass

sys.stdout.reconfigure(encoding="utf-8")
@dataclass(frozen=True)
class BoolTy: pass
@dataclass(frozen=True)
class Arrow: dom: "Ty"; cod: "Ty"
Ty = BoolTy | Arrow; B = BoolTy()
@dataclass(frozen=True)
class Var: name: str
@dataclass(frozen=True)
class BoolLit: value: bool
@dataclass(frozen=True)
class Abs: param: str; param_ty: Ty; body: "Term"
@dataclass(frozen=True)
class App: fn: "Term"; arg: "Term"
@dataclass(frozen=True)
class If: guard: "Term"; yes: "Term"; no: "Term"
Term = Var | BoolLit | Abs | App | If

def infer(t: Term, ctx: dict[str, Ty] | None = None) -> Ty:
    ctx = {} if ctx is None else ctx
    if isinstance(t, Var):
        if t.name not in ctx: raise TypeError(f"未绑定: {t.name}")
        return ctx[t.name]
    if isinstance(t, BoolLit): return B
    if isinstance(t, Abs): return Arrow(t.param_ty, infer(t.body, {**ctx, t.param: t.param_ty}))
    if isinstance(t, App):
        ft, at = infer(t.fn, ctx), infer(t.arg, ctx)
        if not isinstance(ft, Arrow) or ft.dom != at: raise TypeError(f"应用不匹配: {ft} vs {at}")
        return ft.cod
    gt = infer(t.guard, ctx)
    if gt != B: raise TypeError(f"guard 期待 Bool，得到 {gt}")
    yt, nt = infer(t.yes, ctx), infer(t.no, ctx)
    if yt != nt: raise TypeError(f"分支类型不同: {yt} vs {nt}")
    return yt

assert infer(If(BoolLit(True), BoolLit(False), BoolLit(True))) == B  # 正例
try: infer(If(Abs("x", B, Var("x")), BoolLit(True), BoolLit(False)))
except TypeError: pass                                               # 反例
else: raise AssertionError("应拒绝非 Bool guard")
assert infer(Abs("x", B, Var("x"))) == Arrow(B, B)                 # 边界

# 动手改造：为每次递归传入 path，错误中精确报告 guard/yes/no/fn/arg。
print("037 通过：声明式规则已落实为可诊断的类型检查器。")

