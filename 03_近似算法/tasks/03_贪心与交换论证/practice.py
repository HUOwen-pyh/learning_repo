"""带权 Maximum Coverage：边际贪心、穷举与有限 k 的精确保证。"""
from itertools import combinations
from random import Random


def value(chosen, sets, weights):
    covered = set().union(*(sets[i] for i in chosen)) if chosen else set()
    return sum(weights[x] for x in covered)


def greedy(sets, weights, k):
    chosen, covered = [], set()
    for _ in range(min(k, len(sets))):
        i = max((j for j in range(len(sets)) if j not in chosen),
                key=lambda j: sum(weights[x] for x in sets[j] - covered))
        chosen.append(i)
        covered |= sets[i]
    return chosen


def exact(sets, weights, k):
    candidates = (c for r in range(k + 1) for c in combinations(range(len(sets)), r))
    return max(candidates, key=lambda c: value(c, sets, weights))


def self_test():
    rng = Random(314159)
    worst = 1.0
    for n in range(3, 11):
        for _ in range(120):
            m, k = n, rng.randint(1, min(4, n))
            sets = [{x for x in range(n) if rng.random() < .35} for _ in range(m)]
            weights = [rng.randint(1, 7) for _ in range(n)]
            g, o = greedy(sets, weights, k), exact(sets, weights, k)
            gv, ov = value(g, sets, weights), value(o, sets, weights)
            bound = 1 - (1 - 1 / k) ** k
            assert gv + 1e-9 >= bound * ov
            if ov:
                worst = min(worst, gv / ov)
    print(f"guarantee checked; smallest sampled ALG/OPT={worst:.3f}")


if __name__ == "__main__":
    self_test()

# 动手改造：实现 lazy greedy（最大堆保存过期边际上界），并用计数器比较
# 两版的边际计算次数；输出和值必须一致，选择集合可因并列而不同。

