"""枚举半整数 Vertex-Cover LP，阈值舍入并与整数最优对拍。"""
from itertools import product
from random import Random


def feasible(x, edges):
    return all(x[u] + x[v] >= 1 - 1e-12 for u, v in edges)


def half_integral_lp(weights, edges):
    best = None
    for digits in product((0.0, 0.5, 1.0), repeat=len(weights)):
        if feasible(digits, edges):
            cost = sum(w * x for w, x in zip(weights, digits))
            if best is None or cost < best[0]:
                best = (cost, digits)
    return best


def exact_cover(weights, edges):
    n, best = len(weights), None
    for mask in range(1 << n):
        x = [(mask >> v) & 1 for v in range(n)]
        if feasible(x, edges):
            cost = sum(w for v, w in enumerate(weights) if x[v])
            if best is None or cost < best:
                best = cost
    return best


def self_test():
    rng = Random(707)
    for n in range(1, 9):
        for _ in range(40):
            edges = [(u, v) for u in range(n) for v in range(u + 1, n)
                     if rng.random() < .4]
            weights = [rng.randint(1, 9) for _ in range(n)]
            lp, x = half_integral_lp(weights, edges)
            opt = exact_cover(weights, edges)
            rounded = {v for v in range(n) if x[v] >= .5}
            rcost = sum(weights[v] for v in rounded)
            assert all(u in rounded or v in rounded for u, v in edges)
            assert lp <= opt + 1e-9
            assert rcost <= 2 * lp + 1e-9
    n = 7
    clique = [(u, v) for u in range(n) for v in range(u + 1, n)]
    lp, _ = half_integral_lp([1] * n, clique)
    print(f"K_{n}: LP={lp}, OPT={exact_cover([1]*n, clique)}, gap={(n-1)/lp:.3f}")


if __name__ == "__main__":
    self_test()

# 动手改造：对 x=0/1 做 Nemhauser–Trotter 固定，只在 x=1/2 的诱导子图上
# 穷举；比较原始 2^n 与核化后的状态数。

