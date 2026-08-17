"""第066晚：constant fold 的结构归纳实验。动手改造：加入 Mul。"""
from __future__ import annotations
from dataclasses import dataclass
import sys
if hasattr(sys.stdout,"reconfigure"):sys.stdout.reconfigure(encoding="utf-8")
@dataclass(frozen=True)
class Lit:value:int
@dataclass(frozen=True)
class Add:left:object;right:object
@dataclass(frozen=True)
class Neg:e:object
def size(e):
    if isinstance(e,Lit):return 1
    if isinstance(e,Add):return 1+size(e.left)+size(e.right)
    if isinstance(e,Neg):return 1+size(e.e)
    raise TypeError(e)
def ev(e):
    if isinstance(e,Lit):return e.value
    if isinstance(e,Add):return ev(e.left)+ev(e.right)
    if isinstance(e,Neg):return -ev(e.e)
    raise TypeError(e)
def fold(e):
    if isinstance(e,Lit):return e
    if isinstance(e,Neg):
        x=fold(e.e);return Lit(-x.value) if isinstance(x,Lit) else Neg(x)
    if isinstance(e,Add):
        a,b=fold(e.left),fold(e.right)
        return Lit(a.value+b.value) if isinstance(a,Lit) and isinstance(b,Lit) else Add(a,b)
    raise TypeError(e)
def faulty(e):return Lit(0)
def main():
    samples=[Lit(0),Neg(Lit(3)),Add(Lit(1),Neg(Lit(2))),Add(Add(Lit(1),Lit(2)),Lit(3))]
    assert all(ev(fold(e))==ev(e) and size(fold(e))<=size(e) for e in samples)
    assert fold(Lit(0))==Lit(0)                            # base boundary
    assert any(ev(faulty(e))!=ev(e) for e in samples)      # negative implementation
    print("第066晚通过：所有 AST 构造器的 fold 语义保持样本成立。")
if __name__=="__main__":main()
# 动手改造：完成 read.md 验收项中的扩展，并为新规则补一条正例和一条反例。
