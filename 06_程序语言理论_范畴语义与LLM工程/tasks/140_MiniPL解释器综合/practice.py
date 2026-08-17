"""自有 lexer→parser→AST→closure evaluator 的 MiniPL 闭环。"""
from __future__ import annotations

from dataclasses import dataclass
import random
import re
import sys
from typing import TypeAlias

sys.stdout.reconfigure(encoding="utf-8")


@dataclass(frozen=True)
class Token:
    kind: str
    text: str
    pos: int


TOKEN = re.compile(r"\s+|->|[()+*=]|[0-9]+|[A-Za-z_][A-Za-z_0-9]*")


def lex(source: str) -> list[Token]:
    out: list[Token] = []
    pos = 0
    while pos < len(source):
        match = TOKEN.match(source, pos)
        if not match:
            raise SyntaxError(f"unexpected character at {pos}: {source[pos]!r}")
        text = match.group()
        if not text.isspace():
            kind = "NUM" if text.isdigit() else "ID" if text[0].isalpha() or text[0] == "_" else text
            if text in {"let", "in", "fun"}:
                kind = text
            out.append(Token(kind, text, pos))
        pos = match.end()
    out.append(Token("EOF", "", len(source)))
    return out


@dataclass(frozen=True)
class Num:
    value: int


@dataclass(frozen=True)
class Var:
    name: str


@dataclass(frozen=True)
class Add:
    left: "Expr"
    right: "Expr"


@dataclass(frozen=True)
class Mul:
    left: "Expr"
    right: "Expr"


@dataclass(frozen=True)
class Let:
    name: str
    value: "Expr"
    body: "Expr"


@dataclass(frozen=True)
class Lam:
    param: str
    body: "Expr"


@dataclass(frozen=True)
class App:
    function: "Expr"
    argument: "Expr"


Expr: TypeAlias = Num | Var | Add | Mul | Let | Lam | App


class Parser:
    def __init__(self, tokens: list[Token]):
        self.tokens = tokens
        self.i = 0

    def peek(self) -> Token:
        return self.tokens[self.i]

    def take(self, kind: str) -> Token:
        token = self.peek()
        if token.kind != kind:
            raise SyntaxError(f"expected {kind} at {token.pos}, got {token.kind}")
        self.i += 1
        return token

    def parse(self) -> Expr:
        term = self.expr()
        self.take("EOF")
        return term

    def expr(self) -> Expr:
        if self.peek().kind == "let":
            self.take("let")
            name = self.take("ID").text
            self.take("=")
            value = self.expr()
            self.take("in")
            return Let(name, value, self.expr())
        if self.peek().kind == "fun":
            self.take("fun")
            param = self.take("ID").text
            self.take("->")
            return Lam(param, self.expr())
        return self.add()

    def add(self) -> Expr:
        term = self.mul()
        while self.peek().kind == "+":
            self.take("+")
            term = Add(term, self.mul())
        return term

    def mul(self) -> Expr:
        term = self.call()
        while self.peek().kind == "*":
            self.take("*")
            term = Mul(term, self.call())
        return term

    def call(self) -> Expr:
        term = self.atom()
        while self.peek().kind == "(":
            self.take("(")
            argument = self.expr()
            self.take(")")
            term = App(term, argument)
        return term

    def atom(self) -> Expr:
        token = self.peek()
        if token.kind == "NUM":
            self.i += 1
            return Num(int(token.text))
        if token.kind == "ID":
            self.i += 1
            return Var(token.text)
        if token.kind == "(":
            self.take("(")
            term = self.expr()
            self.take(")")
            return term
        raise SyntaxError(f"expected expression at {token.pos}, got {token.kind}")


def parse(source: str) -> Expr:
    return Parser(lex(source)).parse()


@dataclass(frozen=True)
class Closure:
    param: str
    body: Expr
    env: dict[str, "Value"]


Value: TypeAlias = int | Closure


def evaluate(term: Expr, env: dict[str, Value] | None = None) -> Value:
    scope = {} if env is None else env
    if isinstance(term, Num):
        return term.value
    if isinstance(term, Var):
        if term.name not in scope:
            raise NameError(term.name)
        return scope[term.name]
    if isinstance(term, (Add, Mul)):
        left, right = evaluate(term.left, scope), evaluate(term.right, scope)
        if type(left) is not int or type(right) is not int:
            raise TypeError("arithmetic expects integers")
        return left + right if isinstance(term, Add) else left * right
    if isinstance(term, Let):
        value = evaluate(term.value, scope)
        return evaluate(term.body, {**scope, term.name: value})
    if isinstance(term, Lam):
        return Closure(term.param, term.body, dict(scope))
    function = evaluate(term.function, scope)
    if not isinstance(function, Closure):
        raise TypeError("application expects a closure")
    argument = evaluate(term.argument, scope)
    return evaluate(function.body, {**function.env, function.param: argument})


def pretty(term: Expr) -> str:
    if isinstance(term, Num):
        return str(term.value)
    if isinstance(term, Var):
        return term.name
    if isinstance(term, Add):
        return f"({pretty(term.left)} + {pretty(term.right)})"
    if isinstance(term, Mul):
        return f"({pretty(term.left)} * {pretty(term.right)})"
    if isinstance(term, Let):
        return f"(let {term.name} = {pretty(term.value)} in {pretty(term.body)})"
    if isinstance(term, Lam):
        return f"(fun {term.param} -> {pretty(term.body)})"
    return f"{pretty(term.function)}({pretty(term.argument)})"


def generate(rng: random.Random, depth: int) -> Expr:
    if depth == 0:
        return Num(rng.randrange(10))
    cls = rng.choice((Add, Mul))
    return cls(generate(rng, depth - 1), generate(rng, depth - 1))


def main() -> None:
    rng = random.Random(140)
    for _ in range(100):
        original = generate(rng, 3)
        reparsed = parse(pretty(original))
        assert reparsed == original
        assert evaluate(reparsed) == evaluate(original)

    lexical = "let x = 1 in let f = fun y -> x + y in let x = 100 in f(2)"
    assert evaluate(parse(lexical)) == 3
    assert evaluate(parse(" 0 + 2 * 3 ")) == 6
    for bad in ("", "1+", "x+1", "1/0", "True", "()"):
        try:
            evaluate(parse(bad))
        except (SyntaxError, NameError):
            pass
        else:
            raise AssertionError(f"should reject {bad!r}")
    print("100 个 round-trip 差分、优先级、closure 与错误位置测试通过")


if __name__ == "__main__":
    main()

# 动手改造：加入减法构造与一元负号，并为其优先级补正例、反例、边界例。
