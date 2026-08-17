"""极大匹配顶点覆盖：算法、精确 oracle 与随机对拍（Python 3.11+）。"""
from itertools import combinations
from random import Random


def is_cover(n, edges, chosen):
    chosen = set(chosen)
    return all(u in chosen or v in chosen for u, v in edges)


def maximal_matching_cover(n, edges):
    used, matching = set(), []
    for u, v in edges:
        if u not in used and v not in used:
            matching.append((u, v))
            used.update((u, v))
    return used, matching


def exact_vertex_cover(n, edges):
    for size in range(n + 1):
        for picked in combinations(range(n), size):
            if is_cover(n, edges, picked):
                return set(picked)
    raise AssertionError("有限图总有顶点覆盖")


def self_test():
    rng = Random(20260813)
    worst = (0.0, None)
    for n in range(1, 10):
        all_edges = list(combinations(range(n), 2))
        for _ in range(80):
            edges = [e for e in all_edges if rng.random() < 0.28]
            approx, matching = maximal_matching_cover(n, edges)
            optimum = exact_vertex_cover(n, edges)
            assert is_cover(n, edges, approx)
            assert len(matching) <= len(optimum)
            assert len(approx) <= 2 * len(optimum)
            ratio = len(approx) / max(1, len(optimum))
            if ratio > worst[0]:
                worst = (ratio, (n, edges, approx, optimum))
    print(f"random tests passed; observed worst ratio={worst[0]:.3f}")
    print("witness:", worst[1])


if __name__ == "__main__":
    self_test()

# 动手改造：让算法支持带权顶点。先构造反例说明“选匹配两端”不再是
# 2-近似，再思考第 07 晚的 LP 舍入为何能处理权重。

