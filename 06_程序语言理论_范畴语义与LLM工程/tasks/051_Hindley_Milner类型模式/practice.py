"""第051晚：HM 类型模式的自由变量、实例化和泛化。"""
from __future__ import annotations
from dataclasses import dataclass
import sys
if hasattr(sys.stdout, "reconfigure"): sys.stdout.reconfigure(encoding="utf-8")

@dataclass(frozen=True)
class TVar: name: str
@dataclass(frozen=True)
class TCon: name: str
@dataclass(frozen=True)
class TFun:
    left: object
    right: object
@dataclass(frozen=True)
class Scheme:
    quantified: tuple[str, ...]
    body: object

def ftv(t: object) -> set[str]:
    if isinstance(t, TVar): return {t.name}
    if isinstance(t, TCon): return set()
    if isinstance(t, TFun): return ftv(t.left) | ftv(t.right)
    if isinstance(t, Scheme): return ftv(t.body) - set(t.quantified)
    raise TypeError(t)

def subst(t: object, s: dict[str, object]) -> object:
    if isinstance(t, TVar): return s.get(t.name, t)
    if isinstance(t, TCon): return t
    if isinstance(t, TFun): return TFun(subst(t.left, s), subst(t.right, s))
    raise TypeError(t)

class Fresh:
    def __init__(self): self.n = 0
    def one(self) -> TVar:
        v = TVar(f"t{self.n}"); self.n += 1; return v

def instantiate(sc: Scheme, fresh: Fresh) -> object:
    return subst(sc.body, {v: fresh.one() for v in sc.quantified})

def generalize(env: dict[str, Scheme], t: object) -> Scheme:
    env_vars: set[str] = set()
    for sc in env.values(): env_vars |= ftv(sc)
    return Scheme(tuple(sorted(ftv(t) - env_vars)), t)

def main() -> None:
    a, b = TVar("a"), TVar("b")
    identity = Scheme(("a",), TFun(a, a))
    fresh = Fresh()
    i1, i2 = instantiate(identity, fresh), instantiate(identity, fresh)
    assert i1 == TFun(TVar("t0"), TVar("t0"))
    assert i2 == TFun(TVar("t1"), TVar("t1")) and i1 != i2
    env = {"y": Scheme((), b)}
    assert generalize(env, TFun(a, a)).quantified == ("a",)
    assert generalize(env, TFun(b, a)).quantified == ("a",)
    assert generalize({}, TCon("Int")).quantified == ()       # boundary
    assert ftv(Scheme(("a",), TFun(a, b))) == {"b"}           # negative scope check
    print("第051晚通过：实例彼此新鲜，泛化未越过环境边界。")

if __name__ == "__main__": main()
# 动手改造：完成 read.md 验收项中的扩展，并为新规则补一条正例和一条反例。
