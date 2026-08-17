"""第 3 晚：随机化 Quickselect 与比较次数分布。"""

from __future__ import annotations

import sys

sys.stdout.reconfigure(encoding="utf-8")

import random
import statistics


def quickselect(values: list[int], k: int, rng: random.Random) -> tuple[int, int]:
    if not 0 <= k < len(values):
        raise IndexError(k)
    a = values.copy()
    lo, hi, comparisons = 0, len(a), 0
    while True:
        if hi - lo == 1:
            return a[lo], comparisons
        pivot = a[rng.randrange(lo, hi)]
        lt, i, gt = lo, lo, hi
        while i < gt:
            comparisons += 1
            if a[i] < pivot:
                a[lt], a[i] = a[i], a[lt]
                lt += 1
                i += 1
            elif a[i] > pivot:
                gt -= 1
                a[i], a[gt] = a[gt], a[i]
            else:
                i += 1
        assert all(x < pivot for x in a[lo:lt])
        assert all(x == pivot for x in a[lt:gt])
        assert all(x > pivot for x in a[gt:hi])
        if k < lt:
            hi = lt
        elif k >= gt:
            lo = gt
        else:
            return pivot, comparisons


def main() -> None:
    master = random.Random(42)
    counts: list[int] = []
    for case in range(500):
        n = master.randrange(1, 150)
        data = [master.randrange(-20, 21) for _ in range(n)]
        k = master.randrange(n)
        value, comparisons = quickselect(data, k, random.Random(case))
        assert value == sorted(data)[k]
        counts.append(comparisons)
    q95 = statistics.quantiles(counts, n=20)[18]
    print(
        "500 组通过；比较次数",
        f"median={statistics.median(counts):.0f}, p95={q95:.0f}, max={max(counts)}",
    )


if __name__ == "__main__":
    main()

# 动手改造：记录每次保留区间的缩小比例，验证“好枢轴”出现的频率。
