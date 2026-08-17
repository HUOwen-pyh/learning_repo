"""Set Cover 的指数精确 DP 与多项式贪心：经验 gap 不是硬度证明。"""
from random import Random


def exact_cover(universe_size, sets):
    full = (1 << universe_size) - 1
    masks = [sum(1 << x for x in s) for s in sets]
    best = [10**9] * (1 << universe_size)
    best[0] = 0
    for mask in range(1 << universe_size):
        for sm in masks:
            best[mask | sm] = min(best[mask | sm], best[mask] + 1)
    return best[full]


def greedy_cover(universe_size, sets):
    uncovered, chosen = set(range(universe_size)), []
    while uncovered:
        i = max(range(len(sets)), key=lambda j: len(sets[j] & uncovered))
        gain = sets[i] & uncovered
        if not gain:
            raise ValueError("instance is infeasible")
        chosen.append(i)
        uncovered -= gain
    return chosen


def self_test():
    rng = Random(20260813)
    worst = 1.0
    for n in range(2, 11):
        for _ in range(100):
            sets = [{x} for x in range(n)]
            sets += [{x for x in range(n) if rng.random() < 0.35}
                     for _ in range(n + 3)]
            opt = exact_cover(n, sets)
            alg = len(greedy_cover(n, sets))
            assert opt <= alg
            assert alg <= n
            worst = max(worst, alg / opt)
    print(f"all oracle checks passed; largest sampled ALG/OPT={worst:.3f}")


if __name__ == "__main__":
    self_test()

# 动手改造：增加 costs 参数并用“单位成本新覆盖数”贪心；精确 DP 的状态值
# 改成最小成本。加入一个非单位成本实例，让按新覆盖数贪心明确失败。

