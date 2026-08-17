"""source→opt→IR→VM 的分阶段差分、故障注入与最小反例收缩。"""
from __future__ import annotations

from dataclasses import dataclass
import random
import sys
from typing import Callable

sys.stdout.reconfigure(encoding="utf-8")


@dataclass(frozen=True)
class N:
    value: int


@dataclass(frozen=True)
class Add:
    left: "Term"
    right: "Term"


Term = N | Add
Instruction = tuple[str] | tuple[str, int]
Code = list[Instruction]


def evaluate(term: Term) -> int:
    return term.value if isinstance(term, N) else evaluate(term.left) + evaluate(term.right)


def optimize(term: Term) -> Term:
    if isinstance(term, N):
        return term
    left, right = optimize(term.left), optimize(term.right)
    return N(left.value + right.value) if isinstance(left, N) and isinstance(right, N) else Add(left, right)


def compile_ok(term: Term) -> Code:
    if isinstance(term, N):
        return [("PUSH", term.value)]
    return compile_ok(term.left) + compile_ok(term.right) + [("ADD",)]


def compile_mutant(term: Term) -> Code:
    """边界故障：常量达到两位数时 PUSH 少一。"""
    if isinstance(term, N):
        return [("PUSH", term.value - 1 if term.value >= 10 else term.value)]
    return compile_mutant(term.left) + compile_mutant(term.right) + [("ADD",)]


def verify(code: Code) -> bool:
    height = 0
    for instruction in code:
        if instruction[0] == "PUSH":
            height += 1
        elif instruction[0] == "ADD":
            height -= 1
        else:
            return False
        if height < 1:
            return False
    return height == 1


def run_vm(code: Code) -> int:
    stack: list[int] = []
    for instruction in code:
        if instruction[0] == "PUSH":
            stack.append(instruction[1])
        else:
            right, left = stack.pop(), stack.pop()
            stack.append(left + right)
    if len(stack) != 1:
        raise RuntimeError("bad final stack")
    return stack[0]


def failing_stage(term: Term, compiler: Callable[[Term], Code]) -> str | None:
    optimized = optimize(term)
    if evaluate(optimized) != evaluate(term):
        return "optimizer"
    code = compiler(optimized)
    if not verify(code):
        return "verifier"
    if run_vm(code) != evaluate(term):
        return "vm-result"
    return None


def size(term: Term) -> int:
    return 1 if isinstance(term, N) else 1 + size(term.left) + size(term.right)


def candidates(term: Term) -> list[Term]:
    if isinstance(term, N):
        return list({N(0), N(1), N(term.value - 1)}) if term.value > 1 else []
    out: list[Term] = [term.left, term.right, Add(N(0), term.right), Add(term.left, N(0))]
    out += [Add(left, term.right) for left in candidates(term.left)]
    out += [Add(term.left, right) for right in candidates(term.right)]
    return out


def shrink(term: Term, fails: Callable[[Term], bool]) -> Term:
    def measure(candidate: Term) -> tuple[int, int]:
        return size(candidate), evaluate(candidate)

    current = term
    while True:
        smaller = sorted(
            {candidate for candidate in candidates(current) if measure(candidate) < measure(current)},
            key=lambda candidate: (*measure(candidate), repr(candidate)),
        )
        replacement = next((candidate for candidate in smaller if fails(candidate)), None)
        if replacement is None:
            return current
        current = replacement


def generate(rng: random.Random, depth: int) -> Term:
    return N(rng.randrange(20)) if depth == 0 else Add(generate(rng, depth - 1), generate(rng, depth - 1))


def main() -> None:
    rng = random.Random(147)
    for _ in range(300):
        term = generate(rng, rng.randrange(5))
        assert failing_stage(term, compile_ok) is None

    injected = Add(N(9), Add(N(2), N(7)))
    assert failing_stage(injected, compile_mutant) == "vm-result"
    minimal = shrink(injected, lambda term: failing_stage(term, compile_mutant) == "vm-result")
    assert size(minimal) == 3
    assert evaluate(minimal) == 10
    assert failing_stage(minimal, compile_mutant) == "vm-result"
    assert all(
        not ((size(candidate), evaluate(candidate)) < (size(minimal), evaluate(minimal))
             and failing_stage(candidate, compile_mutant) == "vm-result")
        for candidate in candidates(minimal)
    )
    assert not verify([("ADD",)])
    assert not verify([("PUSH", 1), ("PUSH", 2)])
    print(f"300 个正确管线样例通过；mutant 定位=vm-result；结构/数值最小反例={minimal}")


if __name__ == "__main__":
    main()

# 动手改造：加入“交换操作数”mutant 与 Sub 节点，比较结构故障和数值边界故障的最小反例。
