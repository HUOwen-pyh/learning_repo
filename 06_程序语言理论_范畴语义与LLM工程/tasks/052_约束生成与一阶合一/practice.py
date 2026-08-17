"""第052晚：带 occurs check 的一阶类型合一。动手改造：保存约束编号。"""
from __future__ import annotations
from dataclasses import dataclass
import sys
if hasattr(sys.stdout, "reconfigure"): sys.stdout.reconfigure(encoding="utf-8")

@dataclass(frozen=True)
class V: name: str
@dataclass(frozen=True)
class C: name: str
@dataclass(frozen=True)
class F:
    a: object
    b: object

class UnifyError(Exception): pass

def occurs(x: str, t: object) -> bool:
    return isinstance(t, V) and t.name == x or isinstance(t, F) and (occurs(x,t.a) or occurs(x,t.b))

def apply(t: object, s: dict[str, object]) -> object:
    if isinstance(t, V) and t.name in s: return apply(s[t.name], s)
    if isinstance(t, F): return F(apply(t.a,s), apply(t.b,s))
    return t

def unify(eqns: list[tuple[object, object]]) -> dict[str, object]:
    s: dict[str, object] = {}
    work = list(eqns)
    while work:
        raw_left, raw_right = work.pop()
        left, right = apply(raw_left, s), apply(raw_right, s)
        if left == right: continue
        if isinstance(left, V):
            if occurs(left.name, right): raise UnifyError("occurs check")
            s = {k: apply(v, {left.name:right}) for k,v in s.items()} | {left.name:right}
        elif isinstance(right, V):
            work.append((right, left))
        elif isinstance(left, F) and isinstance(right, F):
            work += [(left.a,right.a),(left.b,right.b)]
        elif isinstance(left, C) and isinstance(right, C):
            raise UnifyError(f"constructor clash: {left.name}/{right.name}")
        else:
            raise UnifyError("shape clash")
    return s

def must_fail(eqns):
    try: unify(eqns)
    except UnifyError: return
    raise AssertionError("expected unification failure")

def main() -> None:
    a,b = V("a"),V("b"); INT,BOOL=C("Int"),C("Bool")
    s = unify([(a,F(b,INT)),(b,BOOL)])
    assert apply(a,s) == F(BOOL,INT)
    assert unify([]) == {}                                  # boundary
    must_fail([(INT,BOOL)])                                 # negative clash
    must_fail([(a,F(a,BOOL))])                              # infinite type
    s2 = unify([(F(a,a),F(INT,INT))])
    assert apply(a,s2) == INT
    print("第052晚通过：MGU、空约束、构造冲突与 occurs check 均通过。")

if __name__ == "__main__": main()
# 动手改造：完成 read.md 验收项中的扩展，并为新规则补一条正例和一条反例。
