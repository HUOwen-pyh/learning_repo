"""把最小 STLC AST 翻译成自由 CCC 组合子，并解释到有限集合。"""
from __future__ import annotations
from dataclasses import dataclass
import sys
sys.stdout.reconfigure(encoding="utf-8")

@dataclass(frozen=True)
class Atom:
    name: str

@dataclass(frozen=True)
class Arrow:
    source: object
    target: object

# STLC 项；Var(0) 是最近绑定的变量。
@dataclass(frozen=True)
class Var:
    index: int

@dataclass(frozen=True)
class Lam:
    param_type: object
    body: object

@dataclass(frozen=True)
class App:
    function: object
    argument: object

class TypeErrorSTLC(Exception):
    pass

def infer(term: object, context: tuple[object, ...] = ()) -> object:
    if isinstance(term, Var):
        if term.index < 0 or term.index >= len(context):
            raise TypeErrorSTLC(f"未绑定变量 #{term.index}")
        return context[-1-term.index]
    if isinstance(term, Lam):
        return Arrow(term.param_type, infer(term.body, context+(term.param_type,)))
    if isinstance(term, App):
        function_type = infer(term.function, context)
        argument_type = infer(term.argument, context)
        if not isinstance(function_type, Arrow) or function_type.source != argument_type:
            raise TypeErrorSTLC("application 类型不匹配")
        return function_type.target
    raise TypeErrorSTLC(f"未知 STLC 项：{term!r}")

# 自由 CCC 的组合子。上下文按 Γ×A 表示；闭项上下文是终对象 ()。
@dataclass(frozen=True)
class Id: pass

@dataclass(frozen=True)
class Fst: pass

@dataclass(frozen=True)
class Snd: pass

@dataclass(frozen=True)
class Compose:
    after: object
    before: object

@dataclass(frozen=True)
class PairC:
    left: object
    right: object

@dataclass(frozen=True)
class Curry:
    body: object

@dataclass(frozen=True)
class Eval: pass

def projection(index: int) -> object:
    if index == 0:
        return Snd()
    return Compose(projection(index-1), Fst())

def compile_ccc(term: object) -> object:
    if isinstance(term, Var):
        return projection(term.index)
    if isinstance(term, Lam):
        return Curry(compile_ccc(term.body))
    if isinstance(term, App):
        return Compose(Eval(), PairC(compile_ccc(term.function), compile_ccc(term.argument)))
    raise TypeErrorSTLC(f"无法翻译：{term!r}")

def interpret(combinator: object, value: object) -> object:
    if isinstance(combinator, Id):
        return value
    if isinstance(combinator, Fst):
        return value[0]
    if isinstance(combinator, Snd):
        return value[1]
    if isinstance(combinator, Compose):
        return interpret(combinator.after, interpret(combinator.before, value))
    if isinstance(combinator, PairC):
        return (interpret(combinator.left, value), interpret(combinator.right, value))
    if isinstance(combinator, Curry):
        return lambda argument: interpret(combinator.body, (value, argument))
    if isinstance(combinator, Eval):
        function, argument = value
        return function(argument)
    raise TypeError(combinator)

def must_fail(action) -> None:
    try:
        action()
    except TypeErrorSTLC:
        return
    raise AssertionError("应当拒绝未类型化项")

def main() -> None:
    boolean = Atom("Bool")
    identity = Lam(boolean, Var(0))
    assert infer(identity) == Arrow(boolean, boolean)
    identity_ccc = compile_ccc(identity)
    assert identity_ccc == Curry(Snd())
    identity_fn = interpret(identity_ccc, ())
    assert [identity_fn(x) for x in (False, True)] == [False, True]

    # λx.λy.x：Var(1) 编译成 snd∘fst，确实读取外层变量。
    first = Lam(boolean, Lam(boolean, Var(1)))
    first_fn = interpret(compile_ccc(first), ())
    assert first_fn(True)(False) is True

    # λf.λg.λx.f(g(x))：application 产生 pair、eval 和 composition。
    endo = Arrow(boolean, boolean)
    compose = Lam(endo, Lam(endo, Lam(boolean,
        App(Var(2), App(Var(1), Var(0))))))
    assert infer(compose) == Arrow(endo, Arrow(endo, endo))
    compose_fn = interpret(compile_ccc(compose), ())
    neg = lambda x: not x
    const_true = lambda _x: True
    assert compose_fn(neg)(neg)(False) is False
    assert compose_fn(neg)(const_true)(False) is False

    # CCC 的恒等与复合也在有限语义中满足单位律。
    sample = ((), True)
    assert interpret(Id(), sample) == sample
    assert interpret(Compose(Id(), Snd()), sample) is True
    must_fail(lambda: infer(Var(0)))
    must_fail(lambda: infer(App(identity, Lam(boolean, Var(0)))))
    print("第105晚通过：STLC 变量/lambda/application 已翻译为 CCC curry-eval 组合子。")

if __name__ == "__main__": main()

# 动手改造（小扩展）：加入积类型、pair/fst/snd AST，并复用 PairC/Fst/Snd 完成翻译。
