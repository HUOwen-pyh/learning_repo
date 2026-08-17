"""有限集合间函数数目揭示始末对象。"""
from __future__ import annotations
import sys
sys.stdout.reconfigure(encoding="utf-8")

def function_count(domain_size: int, codomain_size: int) -> int:
    if domain_size == 0: return 1
    return codomain_size ** domain_size

def main() -> None:
    for n in range(5):
        assert function_count(0, n) == 1
        assert function_count(n, 1) == 1
    assert function_count(1, 0) == 0
    candidates = [n for n in range(5) if all(function_count(m, n) == 1 for m in range(5))]
    assert candidates == [1]
    print("有限集合骨架中的末对象大小为1；始对象大小为0")

if __name__ == "__main__": main()

# 动手改造：写 dual_search，交换箭头方向后自动搜索始对象。
