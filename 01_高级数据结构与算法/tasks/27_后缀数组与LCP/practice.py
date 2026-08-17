"""第 27 晚：倍增后缀数组、Kasai LCP 与模式搜索。"""

from __future__ import annotations

import sys

sys.stdout.reconfigure(encoding="utf-8")

import bisect
import random


def suffix_array(s: str) -> list[int]:
    n = len(s)
    sa = list(range(n))
    rank = [ord(ch) for ch in s]
    k = 1
    while k < n:
        sa.sort(key=lambda i: (rank[i], rank[i + k] if i + k < n else -1))
        new = [0] * n
        for j in range(1, n):
            prev, cur = sa[j - 1], sa[j]
            new[cur] = new[prev] + (
                (rank[prev], rank[prev + k] if prev + k < n else -1)
                < (rank[cur], rank[cur + k] if cur + k < n else -1)
            )
        rank = new
        if n and rank[sa[-1]] == n - 1:
            break
        k *= 2
    return sa


def kasai(s: str, sa: list[int]) -> list[int]:
    n = len(s)
    rank = [0] * n
    for r, i in enumerate(sa):
        rank[i] = r
    lcp, h = [0] * n, 0
    for i in range(n):
        r = rank[i]
        if r == 0:
            continue
        j = sa[r - 1]
        while i + h < n and j + h < n and s[i + h] == s[j + h]:
            h += 1
        lcp[r] = h
        h = max(0, h - 1)
    return lcp


def find_occurrences(s: str, sa: list[int], pattern: str) -> list[int]:
    # 教学版创建长度 |P| 的切片；工程版应做无复制比较并复用 LCP。
    keys = [s[i : i + len(pattern)] for i in sa]
    left, right = bisect.bisect_left(keys, pattern), bisect.bisect_right(keys, pattern)
    return sorted(sa[left:right])


def naive_lcp(a: str, b: str) -> int:
    i = 0
    while i < min(len(a), len(b)) and a[i] == b[i]:
        i += 1
    return i


def main() -> None:
    rng = random.Random(27)
    for _ in range(300):
        s = "".join(rng.choice("banana_") for _ in range(rng.randrange(1, 120)))
        sa = suffix_array(s)
        assert sa == sorted(range(len(s)), key=lambda i: s[i:])
        lcp = kasai(s, sa)
        for r in range(1, len(s)):
            assert lcp[r] == naive_lcp(s[sa[r - 1] :], s[sa[r] :])
        pattern = "".join(rng.choice("ban_") for _ in range(rng.randrange(1, 6)))
        expected = [i for i in range(len(s)) if s.startswith(pattern, i)]
        assert find_occurrences(s, sa, pattern) == expected
    print("通过：300 个随机文本的 SA、LCP、模式查询全部差分一致。")


if __name__ == "__main__":
    main()

# 动手改造：用 max(lcp) 返回最长重复子串，并定义并列时的选择规则。
