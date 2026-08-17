"""第011晚：自然数小于等于关系的推导树。"""
from dataclasses import dataclass
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

@dataclass(frozen=True)
class LeZero:
    upper: int

@dataclass(frozen=True)
class LeSucc:
    premise: object

def endpoints(proof: object) -> tuple[int, int]:
    if isinstance(proof, LeZero):
        if proof.upper < 0: raise ValueError("端点不是自然数")
        return 0, proof.upper
    if isinstance(proof, LeSucc):
        left, right = endpoints(proof.premise)
        return left + 1, right + 1
    raise TypeError("未知关系证据")

def build_le(left: int, right: int) -> object | None:
    if left < 0 or right < 0 or left > right: return None
    proof: object = LeZero(right - left)
    for _ in range(left): proof = LeSucc(proof)
    return proof

def main() -> None:
    assert endpoints(LeZero(0)) == (0, 0)                  # 最小正例
    proof = build_le(2, 4)
    assert proof is not None and endpoints(proof) == (2, 4)
    assert build_le(1, 0) is None                          # 最小反例
    for m in range(5):
        for n in range(5):
            assert (build_le(m, n) is not None) == (m <= n)
    print("通过：关系由规则生成证据，不可能端点没有构造路径。")

if __name__ == "__main__": main()

# 动手改造：实现推导树上的 ≤ 传递，并核对组合后的端点。
