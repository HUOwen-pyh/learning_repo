"""第 023 晚：最小算术语言的 lexer、parser 与 AST。"""
from __future__ import annotations

import re
import sys
from dataclasses import dataclass

sys.stdout.reconfigure(encoding="utf-8")


@dataclass(frozen=True)
class Num:
    value: int


@dataclass(frozen=True)
class Bin:
    op: str
    left: "Expr"
    right: "Expr"


Expr = Num | Bin


def lex(source: str) -> list[str]:
    tokens = re.findall(r"\d+|[()+*]", source)
    if "".join(tokens) != re.sub(r"\s+", "", source):
        raise SyntaxError("存在非法字符")
    return tokens


class Parser:
    def __init__(self, tokens: list[str]):
        self.tokens, self.i = tokens, 0

    def peek(self) -> str | None:
        return self.tokens[self.i] if self.i < len(self.tokens) else None

    def take(self, expected: str | None = None) -> str:
        token = self.peek()
        if token is None or (expected is not None and token != expected):
            raise SyntaxError(f"位置 {self.i}: 期待 {expected or 'token'}")
        self.i += 1
        return token

    def expr(self) -> Expr:
        node = self.term()
        while self.peek() == "+":
            self.take("+")
            node = Bin("+", node, self.term())
        return node

    def term(self) -> Expr:
        node = self.atom()
        while self.peek() == "*":
            self.take("*")
            node = Bin("*", node, self.atom())
        return node

    def atom(self) -> Expr:
        token = self.peek()
        if token and token.isdigit():
            return Num(int(self.take()))
        if token == "(":
            self.take("(")
            node = self.expr()
            self.take(")")
            return node
        raise SyntaxError(f"位置 {self.i}: 期待数字或左括号")


def parse(source: str) -> Expr:
    parser = Parser(lex(source))
    tree = parser.expr()
    if parser.peek() is not None:
        raise SyntaxError(f"未消费 token: {parser.peek()}")
    return tree


def evaluate(tree: Expr) -> int:
    if isinstance(tree, Num):
        return tree.value
    a, b = evaluate(tree.left), evaluate(tree.right)
    return a + b if tree.op == "+" else a * b


assert evaluate(parse("2 + 3 * 4")) == 14             # 正例：优先级
assert parse("7") == Num(7)                            # 边界：单 atom
try:                                                    # 反例：缺少右操作数
    parse("2+")
    raise AssertionError("应报告语法错误")
except SyntaxError:
    pass

# 动手改造：加入减法并明确它是左结合，再测试 8-3-2 == 3。
print("023 通过：字符流已被解析为保留优先级的 AST。")

