"""第054晚：存在包检查和隐藏表示。动手改造：公开 make/observe 操作对。"""
from __future__ import annotations
from dataclasses import dataclass
import sys
if hasattr(sys.stdout, "reconfigure"): sys.stdout.reconfigure(encoding="utf-8")

@dataclass(frozen=True)
class TV: name: str
@dataclass(frozen=True)
class Base: name: str
@dataclass(frozen=True)
class Pair:
    left: object
    right: object
@dataclass(frozen=True)
class Exists:
    var: str
    body: object
@dataclass(frozen=True)
class Package:
    witness: object
    value_type: object
    interface: Exists

class PackageError(Exception): pass

def subst(t: object, x: str, r: object) -> object:
    if isinstance(t,TV): return r if t.name==x else t
    if isinstance(t,Pair): return Pair(subst(t.left,x,r),subst(t.right,x,r))
    if isinstance(t,Exists): return t if t.var==x else Exists(t.var,subst(t.body,x,r))
    return t

def check_package(p: Package) -> None:
    expected=subst(p.interface.body,p.interface.var,p.witness)
    if p.value_type != expected:
        raise PackageError(f"expected representation {expected}, got {p.value_type}")

def observe_only_tag(p: Package) -> str:
    check_package(p)
    return "implements existential interface"  # witness is deliberately not returned

def must_fail(p):
    try: check_package(p)
    except PackageError: return
    raise AssertionError("invalid package accepted")

def main() -> None:
    iface=Exists("R",Pair(TV("R"),Base("Observer")))
    nat_impl=Package(Base("Nat"),Pair(Base("Nat"),Base("Observer")),iface)
    text_impl=Package(Base("Text"),Pair(Base("Text"),Base("Observer")),iface)
    check_package(nat_impl); check_package(text_impl)
    assert observe_only_tag(nat_impl)==observe_only_tag(text_impl)
    must_fail(Package(Base("Nat"),Pair(Base("Text"),Base("Observer")),iface))
    empty_iface=Exists("R",Base("Unit"))
    check_package(Package(Base("Nat"),Base("Unit"),empty_iface)) # witness unused boundary
    print("第054晚通过：不同隐藏表示满足同一存在接口，错误包被拒绝。")

if __name__=="__main__": main()
# 动手改造：完成 read.md 验收项中的扩展，并为新规则补一条正例和一条反例。
