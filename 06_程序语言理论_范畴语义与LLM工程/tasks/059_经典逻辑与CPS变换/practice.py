"""第059晚：显式 continuation 和 call/cc 风格逃逸。"""
from __future__ import annotations
from dataclasses import dataclass
import sys
if hasattr(sys.stdout,"reconfigure"):sys.stdout.reconfigure(encoding="utf-8")
@dataclass(frozen=True)
class Num:value:int
@dataclass(frozen=True)
class Add:left:object;right:object
@dataclass(frozen=True)
class Escape:body:object
@dataclass(frozen=True)
class InvokeEscape:value:object
class EvalError(Exception):pass
def direct(e):
    if isinstance(e,Num):return e.value
    if isinstance(e,Add):return direct(e.left)+direct(e.right)
    raise EvalError("control terms require CPS")
def cps(e,k,escape=None):
    if isinstance(e,Num):return k(e.value)
    if isinstance(e,Add):return cps(e.left,lambda a:cps(e.right,lambda b:k(a+b),escape),escape)
    if isinstance(e,Escape):return cps(e.body,k,k)
    if isinstance(e,InvokeEscape):
        if escape is None:raise EvalError("escape outside delimiter")
        return cps(e.value,escape,escape)
    raise EvalError("unknown")
def must_fail(f):
    try:f()
    except EvalError:return
    raise AssertionError("expected control error")
def main():
    ordinary=Add(Num(2),Add(Num(3),Num(4)))
    assert direct(ordinary)==cps(ordinary,lambda x:x)==9
    early=Escape(Add(Num(10),InvokeEscape(Num(7))))
    assert cps(early,lambda x:x)==7
    must_fail(lambda:cps(InvokeEscape(Num(1)),lambda x:x))
    assert cps(Escape(Num(0)),lambda x:x)==0
    print("第059晚通过：CPS 保持普通结果，逃逸 continuation 改变控制流。")
if __name__=="__main__":main()
# 动手改造：完成 read.md 验收项中的扩展，并为新规则补一条正例和一条反例。
