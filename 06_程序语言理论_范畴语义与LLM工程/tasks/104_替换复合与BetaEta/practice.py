"""极小表达式上的替换引理。"""
from __future__ import annotations
from dataclasses import dataclass
import sys
sys.stdout.reconfigure(encoding="utf-8")

@dataclass(frozen=True)
class Var: name: str
@dataclass(frozen=True)
class Add: left: object; right: object
@dataclass(frozen=True)
class Num: value: int

def subst(term, name, value):
    if isinstance(term, Var): return value if term.name == name else term
    if isinstance(term, Add): return Add(subst(term.left,name,value), subst(term.right,name,value))
    return term

def eval_(term, env):
    if isinstance(term, Num): return term.value
    if isinstance(term, Var): return env[term.name]
    return eval_(term.left, env) + eval_(term.right, env)

def main() -> None:
    t, s, env = Add(Var("x"), Var("y")), Add(Var("y"), Num(1)), {"y": 4}
    left = eval_(subst(t, "x", s), env)
    right = eval_(t, {**env, "x": eval_(s, env)})
    assert left == right == 9
    assert subst(Var("z"), "x", Num(0)) == Var("z")
    print("替换引理有限实例:", left, "=", right)

if __name__ == "__main__": main()

# 动手改造：加入 Lambda，并构造会被朴素替换捕获的 (λy.x)[x:=y] 反例。
