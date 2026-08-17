"""第 26 晚：prefix function、KMP 与 Z function。"""

from __future__ import annotations

import sys

sys.stdout.reconfigure(encoding="utf-8")

import random


def prefix_function(s: str) -> list[int]:
    pi = [0] * len(s)
    for i in range(1, len(s)):
        j = pi[i - 1]
        while j and s[i] != s[j]:
            j = pi[j - 1]
        if s[i] == s[j]:
            j += 1
        pi[i] = j
    return pi


def kmp_find(text: str, pattern: str) -> int:
    if pattern == "":
        return 0
    pi, j = prefix_function(pattern), 0
    for i, ch in enumerate(text):
        while j and ch != pattern[j]:
            j = pi[j - 1]
        if ch == pattern[j]:
            j += 1
        if j == len(pattern):
            return i - len(pattern) + 1
    return -1


def z_function(s: str) -> list[int]:
    z = [0] * len(s)
    if s:
        z[0] = len(s)
    left = right = 0
    for i in range(1, len(s)):
        if i < right:
            z[i] = min(right - i, z[i - left])
        while i + z[i] < len(s) and s[z[i]] == s[i + z[i]]:
            z[i] += 1
        if i + z[i] > right:
            left, right = i, i + z[i]
    return z


def naive_z(s: str) -> list[int]:
    out = []
    for i in range(len(s)):
        k = 0
        while i + k < len(s) and s[k] == s[i + k]:
            k += 1
        out.append(k)
    return out


def main() -> None:
    rng, alphabet = random.Random(26), "abca"
    for _ in range(4_000):
        text = "".join(rng.choice(alphabet) for _ in range(rng.randrange(80)))
        pattern = "".join(rng.choice(alphabet) for _ in range(rng.randrange(15)))
        assert kmp_find(text, pattern) == text.find(pattern)
        assert z_function(pattern) == naive_z(pattern)
        pi = prefix_function(pattern)
        for i, length in enumerate(pi):
            assert pattern[:length] == pattern[i - length + 1 : i + 1]
    print("通过：4,000 组 KMP/str.find 与 Z/朴素算法差分一致。")


if __name__ == "__main__":
    main()

# 动手改造：匹配成功后令 j=pi[j-1]，继续扫描以返回所有重叠位置。
