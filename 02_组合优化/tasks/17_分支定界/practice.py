"""第 17 晚：分数背包上界驱动的 best-bound 0-1 背包搜索。"""
from __future__ import annotations
import sys
sys.stdout.reconfigure(encoding="utf-8", errors="backslashreplace")

from dataclasses import dataclass
import heapq
from itertools import product


@dataclass(frozen=True)
class Item:
    index: int
    weight: int
    value: int


@dataclass(frozen=True)
class Node:
    level: int
    weight: int
    value: int
    chosen: tuple[int, ...]


def fractional_bound(node: Node, ordered: list[Item], capacity: int) -> float:
    if node.weight > capacity:
        return float("-inf")
    weight, value = node.weight, float(node.value)
    for item in ordered[node.level:]:
        if weight + item.weight <= capacity:
            weight += item.weight
            value += item.value
        else:
            value += (capacity - weight) * item.value / item.weight
            break
    return value


def branch_and_bound(items: list[Item], capacity: int) -> tuple[int, tuple[int, ...], dict[str, int]]:
    ordered = sorted(items, key=lambda x: x.value / x.weight, reverse=True)
    # 密度贪心得到一个初始可行 incumbent。
    used = best_value = 0
    best_chosen: tuple[int, ...] = ()
    for item in ordered:
        if used + item.weight <= capacity:
            used += item.weight
            best_value += item.value
            best_chosen += (item.index,)
    root = Node(0, 0, 0, ())
    heap: list[tuple[float, int, Node]] = []
    counter = 0
    heapq.heappush(heap, (-fractional_bound(root, ordered, capacity), counter, root))
    stats = {"expanded": 0, "bound_pruned": 0, "infeasible": 0}
    while heap:
        neg_bound, _, node = heapq.heappop(heap)
        if -neg_bound <= best_value + 1e-12:
            stats["bound_pruned"] += 1
            continue
        if node.level == len(ordered):
            continue
        stats["expanded"] += 1
        item = ordered[node.level]
        children = [
            Node(node.level + 1, node.weight + item.weight, node.value + item.value,
                 node.chosen + (item.index,)),
            Node(node.level + 1, node.weight, node.value, node.chosen),
        ]
        for child in children:
            if child.weight > capacity:
                stats["infeasible"] += 1
                continue
            if child.value > best_value:
                best_value, best_chosen = child.value, child.chosen
            bound = fractional_bound(child, ordered, capacity)
            if bound > best_value + 1e-12:
                counter += 1
                heapq.heappush(heap, (-bound, counter, child))
            else:
                stats["bound_pruned"] += 1
    return best_value, tuple(sorted(best_chosen)), stats


def brute(items: list[Item], capacity: int) -> tuple[int, tuple[int, ...]]:
    best = (0, ())
    for bits in product((0, 1), repeat=len(items)):
        weight = sum(i.weight * b for i, b in zip(items, bits))
        value = sum(i.value * b for i, b in zip(items, bits))
        if weight <= capacity and value > best[0]:
            best = (value, tuple(i.index for i, b in zip(items, bits) if b))
    return best


def main() -> None:
    raw = [(9, 16), (6, 12), (12, 22), (7, 13), (3, 6), (11, 17),
           (5, 9), (4, 7), (8, 15), (10, 19), (2, 4), (13, 24)]
    items = [Item(i, w, v) for i, (w, v) in enumerate(raw)]
    capacity = 35
    value, chosen, stats = branch_and_bound(items, capacity)
    truth, _ = brute(items, capacity)
    assert value == truth
    assert sum(items[i].weight for i in chosen) <= capacity
    assert sum(items[i].value for i in chosen) == value
    assert stats["expanded"] < 2 ** len(items)
    print("optimum =", value, "chosen original indices =", chosen)
    print("weight =", sum(items[i].weight for i in chosen))
    print("search statistics =", stats, "versus full leaves =", 2 ** len(items))


if __name__ == "__main__":
    main()

# 动手改造：
# 1. 比较 DFS 与 best-bound 的首个最优解时间、总节点和峰值队列。
# 2. 删除初始贪心 incumbent，量化它对剪枝数的影响。
