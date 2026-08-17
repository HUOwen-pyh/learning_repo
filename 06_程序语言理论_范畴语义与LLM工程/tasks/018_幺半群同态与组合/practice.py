"""第018晚：有限幺半群同态检查与复合。"""
from itertools import product
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

def check_hom(domain, op1, e1, op2, e2, fn):
    if fn(e1) != e2: return False, ("identity", e1)
    for x, y in product(domain, repeat=2):
        if fn(op1(x, y)) != op2(fn(x), fn(y)):
            return False, (x, y)
    return True, None

def main() -> None:
    add4 = lambda a, b: (a + b) % 4
    add2 = lambda a, b: (a + b) % 2
    parity = lambda a: a % 2
    assert check_hom(range(4), add4, 0, add2, 0, parity) == (True, None)
    identity = lambda x: x
    composed = lambda x: identity(parity(x))
    assert check_hom(range(4), add4, 0, add2, 0, composed)[0]
    bad = lambda a: 1 if a else 0
    ok, witness = check_hom(range(4), add4, 0, add2, 0, bad)
    assert not ok and witness is not None                         # 最小反例
    assert check_hom((0,), add4, 0, add2, 0, parity)[0]           # 边界载体
    print(f"通过：模4到模2的 parity 保持结构；坏映射反例={witness}。")

if __name__ == "__main__": main()

# 动手改造：实现“字符串长度”从连接幺半群到加法幺半群的检查。
