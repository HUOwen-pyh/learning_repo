"""第 036 晚：构造 STLC 类型推导树。"""
from __future__ import annotations
import sys
from dataclasses import dataclass

sys.stdout.reconfigure(encoding="utf-8")

@dataclass(frozen=True)
class BoolTy: pass
@dataclass(frozen=True)
class Arrow: dom: "Ty"; cod: "Ty"
Ty = BoolTy | Arrow
B = BoolTy()

@dataclass(frozen=True)
class Var: name: str
@dataclass(frozen=True)
class Abs: param: str; param_ty: Ty; body: "Term"
@dataclass(frozen=True)
class App: fn: "Term"; arg: "Term"
Term = Var | Abs | App

@dataclass(frozen=True)
class Derivation:
    rule: str; term: Term; ty: Ty; premises: tuple["Derivation", ...] = ()

def derive(ctx: dict[str, Ty], t: Term) -> Derivation:
    if isinstance(t, Var):
        if t.name not in ctx: raise TypeError(f"未绑定变量 {t.name}")
        return Derivation("T-Var", t, ctx[t.name])
    if isinstance(t, Abs):
        body = derive({**ctx, t.param: t.param_ty}, t.body)
        return Derivation("T-Abs", t, Arrow(t.param_ty, body.ty), (body,))
    fn, arg = derive(ctx, t.fn), derive(ctx, t.arg)
    if not isinstance(fn.ty, Arrow) or fn.ty.dom != arg.ty:
        raise TypeError("T-App 的定义域与实参不匹配")
    return Derivation("T-App", t, fn.ty.cod, (fn, arg))

identity = Abs("x", B, Var("x"))
assert derive({}, identity).ty == Arrow(B, B)                   # 正例
try: derive({}, App(identity, identity))                        # 反例
except TypeError: pass
else: raise AssertionError("应拒绝错类型应用")
shadow = Abs("x", B, Var("x"))
assert derive({"x": Arrow(B, B)}, shadow).ty == Arrow(B, B)    # 边界：遮蔽

# 动手改造：加入 BoolLit 与 If，并让推导树保存三条 premise。
print("036 通过：typing judgment 已生成可检查的推导对象。")

