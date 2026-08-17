"""第01晚：编码长度与增长率实验。仅用标准库。"""
from math import log2

def linear_steps(n: int) -> int:
    return sum(1 for _ in range(n))

def quadratic_steps(n: int) -> int:
    return sum(1 for _ in range(n) for _ in range(n))

def subset_steps(n: int) -> int:
    return 1 << n

def pseudo_polynomial_steps(value: int) -> int:
    # 操作计数足以说明增长，无需真的循环 value 次。
    return value

def ratios(counter, sizes):
    values = [counter(n) for n in sizes]
    return values, [values[i + 1] / values[i] for i in range(len(values) - 1)]

if __name__ == "__main__":
    sizes = [4, 8, 16]
    for name, fn in [("n", linear_steps), ("n^2", quadratic_steps), ("2^n", subset_steps)]:
        vals, rs = ratios(fn, sizes)
        print(f"{name:4} values={vals}, successive ratios={rs}")
    for value in [15, 255, 65535]:
        bits = value.bit_length()
        print(f"N={value:5}, input bits={bits:2}, N-steps={pseudo_polynomial_steps(value)}, "
              f"steps/bit={value / bits:.1f}")
        assert value < 2 ** bits
    assert quadratic_steps(10) == 100
    assert subset_steps(10) == 1024
    # 动手改造：以 k=4..24 生成 N=2^k-1，画表解释“对数值线性、对输入指数”。

