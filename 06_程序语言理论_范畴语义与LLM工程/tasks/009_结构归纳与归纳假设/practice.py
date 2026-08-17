"""第009晚：把求和恒等式的归纳证明做成可检查链。"""
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

def sum_to(n: int) -> int:
    if n < 0: raise ValueError
    return 0 if n == 0 else sum_to(n - 1) + n

def proposition(n: int) -> bool:
    return 2 * sum_to(n) == n * (n + 1)

def induction_certificate(n: int) -> tuple[bool, ...]:
    """每个条目代表从上一实例到下一实例的已核验归纳步。"""
    if n < 0: raise ValueError
    checks = [proposition(0)]
    for k in range(n):
        ih = proposition(k)
        step = ih and 2 * (sum_to(k) + k + 1) == (k + 1) * (k + 2)
        checks.append(step)
    return tuple(checks)

def main() -> None:
    assert induction_certificate(0) == (True,)              # 最小正例
    assert all(induction_certificate(20))
    assert proposition(100)
    try: induction_certificate(-1)                          # 最小反例
    except ValueError: pass
    else: raise AssertionError("非法归纳指标被接受")
    assert 2 * (sum_to(3) + 4) != 4 * 6                    # 错误结论反例
    print("通过：证书分开基础步与每个后继步；枚举仍不是元层证明。")

if __name__ == "__main__": main()

# 动手改造：为列表长度与拼接的等式实现同样的结构归纳证书。
