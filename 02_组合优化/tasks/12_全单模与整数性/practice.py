"""第 12 晚：枚举全部子式验证 TU，并输出非 TU 证据。"""
from __future__ import annotations
import sys
sys.stdout.reconfigure(encoding="utf-8", errors="backslashreplace")

from itertools import combinations


def determinant(matrix: list[list[int]]) -> int:
    n = len(matrix)
    if n == 0:
        return 1
    if n == 1:
        return matrix[0][0]
    return sum(
        ((-1) ** j) * matrix[0][j]
        * determinant([row[:j] + row[j + 1:] for row in matrix[1:]])
        for j in range(n)
    )


def tu_certificate(matrix: list[list[int]]) -> tuple[bool, tuple[tuple[int, ...], tuple[int, ...], int] | None]:
    rows, cols = len(matrix), len(matrix[0])
    for size in range(1, min(rows, cols) + 1):
        for rs in combinations(range(rows), size):
            for cs in combinations(range(cols), size):
                minor = [[matrix[r][c] for c in cs] for r in rs]
                det = determinant(minor)
                if det not in (-1, 0, 1):
                    return False, (rs, cs, det)
    return True, None


def main() -> None:
    # K_{2,2} 的 0/1 点边关联矩阵：列依次为 00,01,10,11。
    bipartite = [
        [1, 1, 0, 0],
        [0, 0, 1, 1],
        [1, 0, 1, 0],
        [0, 1, 0, 1],
    ]
    is_tu, witness = tu_certificate(bipartite)
    assert is_tu and witness is None

    # 三角形无向点边关联矩阵的行列式绝对值为 2。
    triangle = [
        [1, 1, 0],
        [1, 0, 1],
        [0, 1, 1],
    ]
    is_tu, witness = tu_certificate(triangle)
    assert not is_tu and witness is not None and abs(witness[2]) == 2
    half = [0.5, 0.5, 0.5]
    degrees = [sum(row[j] * half[j] for j in range(3)) for row in triangle]
    assert degrees == [1.0, 1.0, 1.0]
    # 三角形不存在完美匹配，说明这个分数解不是整数解的凸组合。
    assert not any(
        all(sum(row[j] * bits[j] for j in range(3)) == 1 for row in triangle)
        for bits in __import__("itertools").product((0, 1), repeat=3)
    )
    print("K2,2 incidence matrix: TU verified by all minors")
    print("triangle non-TU witness (rows, cols, det) =", witness)
    print("fractional degree-one solution =", half)


if __name__ == "__main__":
    main()

# 动手改造：
# 1. 生成一个有向图节点-弧矩阵，验证删任意一行后仍 TU。
# 2. 给 TU 矩阵添加一条业务行，自动寻找最小破坏子式。
