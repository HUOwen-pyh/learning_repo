"""第050晚：最小双向类型检查器。动手改造：加入 Unit 或 Pair。"""
from __future__ import annotations
from dataclasses import dataclass
import sys
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

Ty = str | tuple

@dataclass(frozen=True)
class Var: name: str
@dataclass(frozen=True)
class Lit: value: bool | int
@dataclass(frozen=True)
class Lam:
    param: str
    body: object
@dataclass(frozen=True)
class Ann:
    term: object
    ty: Ty
@dataclass(frozen=True)
class App:
    fn: object
    arg: object
@dataclass(frozen=True)
class If:
    cond: object
    yes: object
    no: object

BOOL, NAT = "Bool", "Nat"
def arrow(a: Ty, b: Ty) -> Ty: return ("->", a, b)

class TypeError_(Exception): pass

def check(term: object, expected: Ty, env: dict[str, Ty]) -> None:
    if isinstance(term, Lam) and isinstance(expected, tuple) and expected[0] == "->":
        check(term.body, expected[2], {**env, term.param: expected[1]})
        return
    actual = synth(term, env)
    if actual != expected:
        raise TypeError_(f"expected {expected}, got {actual}")

def synth(term: object, env: dict[str, Ty]) -> Ty:
    if isinstance(term, Var):
        if term.name not in env: raise TypeError_(f"unbound {term.name}")
        return env[term.name]
    if isinstance(term, Lit):
        return BOOL if isinstance(term.value, bool) else NAT
    if isinstance(term, Ann):
        check(term.term, term.ty, env); return term.ty
    if isinstance(term, App):
        ft = synth(term.fn, env)
        if not (isinstance(ft, tuple) and ft[0] == "->"):
            raise TypeError_("application of non-function")
        check(term.arg, ft[1], env); return ft[2]
    if isinstance(term, If):
        check(term.cond, BOOL, env)
        yt = synth(term.yes, env)
        check(term.no, yt, env); return yt
    raise TypeError_("cannot synthesize: add an annotation or check against a type")

def must_fail(thunk) -> None:
    try: thunk()
    except TypeError_: return
    raise AssertionError("expected a type error")

def main() -> None:
    ident = Lam("x", Var("x"))
    check(ident, arrow(BOOL, BOOL), {})
    assert synth(App(Ann(ident, arrow(NAT, NAT)), Lit(0)), {}) == NAT
    assert synth(If(Lit(True), Lit(1), Lit(2)), {}) == NAT
    must_fail(lambda: synth(Lam("x", Var("x")), {}))       # boundary
    must_fail(lambda: synth(Var("missing"), {}))             # negative
    must_fail(lambda: synth(If(Lit(0), Lit(1), Lit(2)), {}))
    print("第050晚通过：双向类型检查的正例、反例与边界例均成立。")

if __name__ == "__main__":
    main()
# 动手改造：完成 read.md 验收项中的扩展，并为新规则补一条正例和一条反例。
