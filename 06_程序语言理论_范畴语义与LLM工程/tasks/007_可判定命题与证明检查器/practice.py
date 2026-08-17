"""第007晚：命题 AST 的有效性判定与反例证书。"""
from __future__ import annotations
from dataclasses import dataclass
from itertools import product
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

@dataclass(frozen=True)
class Var: name: str
@dataclass(frozen=True)
class Not: value: object
@dataclass(frozen=True)
class And: left: object; right: object
@dataclass(frozen=True)
class Imp: left: object; right: object

def atoms(f: object) -> set[str]:
    if isinstance(f, Var): return {f.name}
    if isinstance(f, Not): return atoms(f.value)
    if isinstance(f, (And, Imp)): return atoms(f.left) | atoms(f.right)
    raise TypeError("未知公式")

def evaluate(f: object, env: dict[str, bool]) -> bool:
    if isinstance(f, Var): return env[f.name]
    if isinstance(f, Not): return not evaluate(f.value, env)
    if isinstance(f, And): return evaluate(f.left, env) and evaluate(f.right, env)
    if isinstance(f, Imp): return not evaluate(f.left, env) or evaluate(f.right, env)
    raise TypeError("未知公式")

def decide_valid(f: object) -> tuple[bool, dict[str, bool] | None]:
    names = sorted(atoms(f))
    for bits in product((False, True), repeat=len(names)):
        env = dict(zip(names, bits))
        if not evaluate(f, env):
            return False, env
    return True, None

def main() -> None:
    p, q = Var("P"), Var("Q")
    valid, counter = decide_valid(Imp(And(p, q), p))
    assert valid and counter is None                           # 最小正例
    valid, counter = decide_valid(Imp(p, q))
    assert not valid and counter == {"P": True, "Q": False}  # 最小反例
    assert decide_valid(Imp(p, p)) == (True, None)
    print("通过：有效式有穷尽证书；失败式返回可重放的反例赋值。")

if __name__ == "__main__":
    main()

# 动手改造：加入 Or，并让检查器重新求值确认返回的反例确实为假。
