"""加权 Max-Cut 的 1-flip 局部搜索，含局部性和精确值断言。"""
from random import Random


def cut_value(side, edges):
    return sum(w for u, v, w in edges if side[u] != side[v])


def flip_gain(v, side, edges):
    return sum(w if side[v] == side[u if v != u else x] else -w
               for u, x, w in edges if v in (u, x))


def local_search(n, edges, initial=None):
    side = list(initial) if initial is not None else [False] * n
    steps = 0
    while True:
        gains = [flip_gain(v, side, edges) for v in range(n)]
        best = max(range(n), key=gains.__getitem__)
        if gains[best] <= 0:
            return side, steps
        before = cut_value(side, edges)
        side[best] = not side[best]
        steps += 1
        assert cut_value(side, edges) > before


def exact_max_cut(n, edges):
    return max(cut_value([(mask >> v) & 1 for v in range(n)], edges)
               for mask in range(1 << max(0, n - 1)))


def self_test():
    rng = Random(271828)
    worst = 1.0
    for n in range(2, 11):
        for _ in range(80):
            edges = [(u, v, rng.randint(1, 9)) for u in range(n)
                     for v in range(u + 1, n) if rng.random() < .35]
            side, steps = local_search(n, edges)
            alg, opt = cut_value(side, edges), exact_max_cut(n, edges)
            assert all(flip_gain(v, side, edges) <= 0 for v in range(n))
            assert alg * 2 >= sum(w for _, _, w in edges)
            assert alg * 2 >= opt
            assert steps <= sum(w for _, _, w in edges)
            if opt:
                worst = min(worst, alg / opt)
    print(f"local optima verified; smallest sampled ratio={worst:.3f}")


if __name__ == "__main__":
    self_test()

# 动手改造：从 20 个随机初始割重启，比较“最佳一次”与全 False 初值；再加入
# 一个枚举搜索，找出 n<=8 时确实存在的非全局 1-flip 局部最优。

