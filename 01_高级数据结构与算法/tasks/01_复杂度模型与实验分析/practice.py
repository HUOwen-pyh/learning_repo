"""第 1 晚：用操作计数与计时观察增长阶。Python 3.11+。"""

from __future__ import annotations

import sys

sys.stdout.reconfigure(encoding="utf-8")

import random
import statistics
import time


def linear_search(a: list[int], target: int) -> tuple[int, int]:
    comparisons = 0
    for i, value in enumerate(a):
        comparisons += 1
        if value == target:
            return i, comparisons
    return -1, comparisons


def binary_search(a: list[int], target: int) -> tuple[int, int]:
    lo, hi, comparisons = 0, len(a), 0
    while lo < hi:
        mid = (lo + hi) // 2
        comparisons += 1
        if a[mid] < target:
            lo = mid + 1
        elif a[mid] > target:
            hi = mid
        else:
            return mid, comparisons
    return -1, comparisons


def median_sort_time(n: int, repeats: int = 7) -> float:
    rng = random.Random(20260813 + n)
    sample = [rng.randrange(10 * n) for _ in range(n)]
    measurements = []
    for _ in range(repeats):
        data = sample.copy()  # 两个规模使用各自固定输入
        start = time.perf_counter_ns()
        data.sort()
        measurements.append((time.perf_counter_ns() - start) / 1e6)
        assert data == sorted(sample)
    return statistics.median(measurements)


def main() -> None:
    rng = random.Random(7)
    print("n\t线性最坏比较\t二分最坏比较\t排序中位数(ms)")
    for n in (1_000, 2_000, 4_000, 8_000):
        data = list(range(n))
        li, lc = linear_search(data, n - 1)
        bi, bc = binary_search(data, n - 1)
        assert li == bi == n - 1
        assert lc == n and bc <= n.bit_length()
        # 再做若干存在/不存在查询，与 Python 的真值差分核对。
        for target in [rng.randrange(n), -1, n]:
            idx, _ = binary_search(data, target)
            assert (idx != -1) == (target in data)
        print(f"{n}\t{lc}\t\t{bc}\t\t{median_sort_time(n):.3f}")
    print("通过：计数不变量和差分测试。")


if __name__ == "__main__":
    main()

# 动手改造：加入 exponential_search，并记录目标靠近开头时的比较次数。
