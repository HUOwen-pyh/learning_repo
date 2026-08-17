"""研究边序对极大匹配 2-近似的影响，并自动验证紧界。"""
from itertools import combinations, permutations


def cover_from_order(edges):
    used, matching = set(), []
    for u, v in edges:
        if u not in used and v not in used:
            used.update((u, v)); matching.append((u, v))
    return used, matching


def exact_cover(n, edges):
    for r in range(n + 1):
        for c in combinations(range(n), r):
            s = set(c)
            if all(u in s or v in s for u, v in edges):
                return s
    raise AssertionError


def all_order_sizes(n, edges):
    # 教学实例边少，枚举边序；生产环境绝不能这样做。
    return {len(cover_from_order(order)[0]) for order in permutations(edges)}


def self_test():
    star = [(0, i) for i in range(1, 6)]
    c, m = cover_from_order(star)
    assert len(c) == 2 and len(exact_cover(6, star)) == 1
    assert all_order_sizes(6, star) == {2}

    graph = [(0, 1), (1, 2), (2, 3), (0, 3), (3, 4)]
    opt = exact_cover(5, graph)
    sizes = all_order_sizes(5, graph)
    for order in permutations(graph):
        cover, matching = cover_from_order(order)
        assert all(u in cover or v in cover for u, v in graph)
        assert len(matching) <= len(opt)
        assert len(cover) <= 2 * len(opt)
    triangle = [(0, 1), (1, 2), (0, 2)]
    assert len(cover_from_order(triangle)[1]) == 1
    assert len(exact_cover(3, triangle)) == 2
    print("star ratio=2; order-dependent sizes on second graph:", sorted(sizes))


if __name__ == "__main__":
    self_test()

# 动手改造：不枚举全排列，改为 1000 次固定种子的 shuffle；统计解大小直方图，
# 并搜索一个 n<=7、至少出现两种输出大小的最小图。

