"""同一 AST 的变量集合与使用次数 coeffect。"""
from __future__ import annotations
from collections import Counter
from dataclasses import dataclass
import sys
sys.stdout.reconfigure(encoding="utf-8")

@dataclass(frozen=True)
class Var: name:str
@dataclass(frozen=True)
class App: fn:object; arg:object
@dataclass(frozen=True)
class Pair: left:object; right:object

def usage(t):
    if isinstance(t,Var): return Counter({t.name:1})
    if isinstance(t,(App,Pair)): return usage(t.fn if isinstance(t,App) else t.left)+usage(t.arg if isinstance(t,App) else t.right)
    raise TypeError(t)

def main() -> None:
    t=Pair(App(Var("f"),Var("x")),App(App(Var("g"),Var("x")),Var("y")))
    counts=usage(t)
    assert set(counts)=={"f","g","x","y"}
    assert counts["x"]==2 and counts["y"]==1
    assert usage(Var("z")) == Counter({"z": 1})
    print("需求集合=",set(counts),"使用次数=",dict(counts))

if __name__ == "__main__": main()

# 动手改造：加入 Lambda，分别实现自由变量集合与绑定变量使用次数。
