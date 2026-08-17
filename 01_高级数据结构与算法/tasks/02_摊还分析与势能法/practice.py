"""第 2 晚：动态数组的真实成本与势能法。"""

from __future__ import annotations

import sys

sys.stdout.reconfigure(encoding="utf-8")


class DynamicArray:
    def __init__(self) -> None:
        self.size = 0
        self.capacity = 1
        self.buf: list[int | None] = [None]
        self.total_actual_cost = 0

    def append(self, value: int) -> int:
        cost = 1  # 写入新值
        if self.size == self.capacity:
            old = self.buf
            self.capacity *= 2
            self.buf = [None] * self.capacity
            for i in range(self.size):
                self.buf[i] = old[i]
            cost += self.size
        self.buf[self.size] = value
        self.size += 1
        self.total_actual_cost += cost
        self._check()
        return cost

    def potential(self) -> int:
        return 2 * self.size - self.capacity + 1

    def values(self) -> list[int]:
        return [x for x in self.buf[: self.size] if x is not None]

    def _check(self) -> None:
        assert 0 <= self.size <= self.capacity
        assert self.capacity >= 1 and self.capacity & (self.capacity - 1) == 0


def main() -> None:
    a = DynamicArray()
    reference: list[int] = []
    old_phi = a.potential()
    total_amortized = 0
    worst = (0, 0)
    print("i\t容量\t实际成本\t摊还成本\t势能")
    for i in range(1, 65):
        actual = a.append(i)
        reference.append(i)
        phi = a.potential()
        amortized = actual + phi - old_phi
        total_amortized += amortized
        old_phi = phi
        worst = max(worst, (actual, i))
        if i <= 10 or i & (i - 1) == 0:
            print(f"{i}\t{a.capacity}\t{actual}\t\t{amortized}\t\t{phi}")
        assert a.values() == reference
        assert amortized <= 3
    assert a.total_actual_cost < 3 * a.size
    assert total_amortized == a.total_actual_cost + a.potential()
    print(f"通过：64 次追加实际总成本={a.total_actual_cost}，最大单次={worst}。")


if __name__ == "__main__":
    main()

# 动手改造：实现增长因子 1.5（注意取整和必须增长），比较复制总量与峰值空槽。
