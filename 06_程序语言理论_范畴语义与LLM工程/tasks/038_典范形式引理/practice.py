"""第 038 晚：可执行的 canonical-forms 检查。"""
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
class BoolLit: value: bool
@dataclass(frozen=True)
class Var: name: str
@dataclass(frozen=True)
class Abs: param: str; param_ty: Ty; body: "Term"
@dataclass(frozen=True)
class App: fn: "Term"; arg: "Term"
Term = BoolLit | Var | Abs | App

def infer(t: Term, ctx: dict[str, Ty] | None = None) -> Ty:
    ctx = {} if ctx is None else ctx
    if isinstance(t, BoolLit): return B
    if isinstance(t, Var):
        if t.name not in ctx: raise TypeError("开放变量")
        return ctx[t.name]
    if isinstance(t, Abs):
        return Arrow(t.param_ty, infer(t.body, {**ctx, t.param: t.param_ty}))
    fn_ty, arg_ty = infer(t.fn, ctx), infer(t.arg, ctx)
    if not isinstance(fn_ty, Arrow) or fn_ty.dom != arg_ty:
        raise TypeError("错误应用")
    return fn_ty.cod

def is_value(t: Term) -> bool:
    return isinstance(t, (BoolLit, Abs))

def canonical(t: Term, claimed: Ty) -> str:
    actual = infer(t, {})
    if actual != claimed: raise TypeError("类型证据与项不匹配")
    if not is_value(t): raise ValueError("canonical forms 的 premise 要求 value")
    if claimed == B and isinstance(t, BoolLit): return "boolean-literal"
    if isinstance(claimed, Arrow) and isinstance(t, Abs): return "lambda"
    raise AssertionError("良类型值违反典范形式")

identity = Abs("x", B, Var("x"))
assert canonical(identity, Arrow(B, B)) == "lambda"            # 正例
try: canonical(identity, B)                                    # 反例
except TypeError: pass
else: raise AssertionError("应拒绝伪造类型")
assert canonical(BoolLit(False), B) == "boolean-literal"       # 边界
nested = Abs("x", B, Abs("y", B, Var("x")))
assert canonical(nested, Arrow(B, Arrow(B, B))) == "lambda"    # 合法嵌套闭项
try: canonical(App(identity, BoolLit(True)), B)                  # 良类型但不是 value
except ValueError: pass
else: raise AssertionError("canonical forms 不适用于非 value")

# 动手改造：让 infer_closed 支持 App，并明确 App 永远不是本语言的 value。
print("038 通过：类型与 value 条件共同决定了典范外形。")
