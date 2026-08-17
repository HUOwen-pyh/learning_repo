"""第071晚：组合式表达式指称。动手改造：加入 Mul。"""
from __future__ import annotations
from dataclasses import dataclass
import sys
if hasattr(sys.stdout,"reconfigure"):sys.stdout.reconfigure(encoding="utf-8")
@dataclass(frozen=True)
class Num:value:int
@dataclass(frozen=True)
class Var:name:str
@dataclass(frozen=True)
class Add:left:object;right:object
def denote(e):
    if isinstance(e,Num):return lambda env:e.value
    if isinstance(e,Var):return lambda env:env[e.name]
    if isinstance(e,Add):
        l,r=denote(e.left),denote(e.right)
        return lambda env:l(env)+r(env)
    raise TypeError(e)
def main():
    e=Add(Var("x"),Num(1));rho={"x":4,"unused":99}
    assert denote(e)(rho)==5
    assert denote(Num(7))({})==7                       # environment-free boundary
    assert denote(e)({"x":4})==denote(e)(rho)          # unused variable irrelevance
    try:denote(Var("missing"))({})
    except KeyError:pass
    else:raise AssertionError("unbound variable accepted")
    print("第071晚通过：表达式含义按语法组合且只依赖自由变量。")
if __name__=="__main__":main()
# 动手改造：完成 read.md 验收项中的扩展，并为新规则补一条正例和一条反例。
