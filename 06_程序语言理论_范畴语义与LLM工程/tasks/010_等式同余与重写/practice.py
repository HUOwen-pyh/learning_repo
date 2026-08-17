"""第010晚：显式端点的等式证明链。"""
from dataclasses import dataclass
from collections.abc import Callable
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

@dataclass(frozen=True)
class Equality:
    left: object
    right: object
    reason: str

def refl(x: object) -> Equality:
    return Equality(x, x, "refl")

def sym(eq: Equality) -> Equality:
    return Equality(eq.right, eq.left, f"sym({eq.reason})")

def trans(first: Equality, second: Equality) -> Equality:
    if first.right != second.left: raise ValueError("等式链断裂")
    return Equality(first.left, second.right, f"{first.reason};{second.reason}")

def cong(fn: Callable[[object], object], eq: Equality) -> Equality:
    return Equality(fn(eq.left), fn(eq.right), f"cong({eq.reason})")

def main() -> None:
    e1, e2 = Equality(1 + 1, 2, "计算"), Equality(2, 4 // 2, "计算")
    assert trans(e1, e2).left == trans(e1, e2).right       # 最小正例
    assert cong(lambda x: (x, x), e1).left == (2, 2)
    twice = sym(sym(e1))
    assert (twice.left, twice.right) == (e1.left, e1.right)
    try: trans(Equality(0, 1, "假设"), Equality(2, 3, "假设"))
    except ValueError: pass                                # 最小反例
    else: raise AssertionError("断裂等式链被接受")
    assert refl("x").left == refl("x").right
    print("通过：重写保存端点，传递只接受首尾相接的证明。")

if __name__ == "__main__": main()

# 动手改造：实现一条 rewrite(value, equality, direction) 并检查方向。
