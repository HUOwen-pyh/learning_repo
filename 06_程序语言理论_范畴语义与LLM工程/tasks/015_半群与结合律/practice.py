"""第015晚：有限载体上的半群定律检查与反例。"""
from itertools import product
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

def associative(values, op):
    for a, b, c in product(values, repeat=3):
        if op(op(a, b), c) != op(a, op(b, c)):
            return False, (a, b, c)
    return True, None

def main() -> None:
    ok, witness = associative(range(4), lambda a, b: max(a, b))
    assert ok and witness is None                              # 最小正例
    ok, witness = associative(range(3), lambda a, b: (a + b) % 3)
    assert ok
    ok, witness = associative(range(3), lambda a, b: a - b)
    assert not ok and witness is not None                      # 最小反例
    a, b, c = witness
    assert (a - b) - c != a - (b - c)
    assert "a" + "b" != "b" + "a"                           # 半群不必交换
    print(f"通过：减法结合律反例={witness}；结合不蕴含交换。")

if __name__ == "__main__": main()

# 动手改造：返回字典序最小反例，并检查矩阵乘法的小型有限样本。
