"""第055晚：用语法值分类器演示 value restriction。"""
from __future__ import annotations
from dataclasses import dataclass
import sys
if hasattr(sys.stdout, "reconfigure"): sys.stdout.reconfigure(encoding="utf-8")

@dataclass(frozen=True)
class Var: name:str
@dataclass(frozen=True)
class Lit: value:object
@dataclass(frozen=True)
class Lam:
    var:str
    body:object
@dataclass(frozen=True)
class Tuple_: items:tuple[object,...]
@dataclass(frozen=True)
class App:
    f:object
    x:object
@dataclass(frozen=True)
class Ref: value:object

def is_value(e:object)->bool:
    if isinstance(e,(Var,Lit,Lam)): return True
    if isinstance(e,Tuple_): return all(is_value(x) for x in e.items)
    return False

def may_generalize(e:object, free_in_env:set[str], free_in_type:set[str])->set[str]:
    return free_in_type-free_in_env if is_value(e) else set()

def main()->None:
    ident=Lam("x",Var("x"))
    assert may_generalize(ident,set(),{"a"})=={"a"}
    assert may_generalize(App(ident,Lit(0)),set(),{"a"})==set() # effectful computation form
    assert may_generalize(Ref(ident),set(),{"a"})==set()        # dangerous allocation
    assert may_generalize(ident,{"a"},{"a","b"})=={"b"}        # environment boundary
    assert is_value(Tuple_(()))                                # empty-product boundary
    assert is_value(Tuple_((Lit(1),ident)))
    assert not is_value(Tuple_((Lit(1),Ref(ident))))            # negative nested case
    print("第055晚通过：值可泛化，引用分配和应用不可泛化。")

if __name__=="__main__": main()
# 动手改造：完成 read.md 验收项中的扩展，并为新规则补一条正例和一条反例。
