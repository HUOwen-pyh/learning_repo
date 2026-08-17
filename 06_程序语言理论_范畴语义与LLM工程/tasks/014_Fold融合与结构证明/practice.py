"""第014晚：检查 fold 融合的局部条件并差分测试。"""
from itertools import product
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

def foldr(step, base, xs):
    result = base
    for x in reversed(xs): result = step(x, result)
    return result

def fusion_holds(h, step, base, step2, base2, values, accumulators) -> bool:
    return h(base) == base2 and all(
        h(step(x, y)) == step2(x, h(y)) for x in values for y in accumulators
    )

def main() -> None:
    h = lambda n: 2 * n
    step = lambda x, acc: x + acc
    step2 = lambda x, acc: 2 * x + acc
    assert fusion_holds(h, step, 0, step2, 0, range(4), range(7))
    for size in range(5):
        for xs in product(range(3), repeat=size):
            left = h(foldr(step, 0, xs))
            right = foldr(step2, 0, xs)
            assert left == right                              # 正例族
    bad_step = lambda x, acc: x + acc
    assert not fusion_holds(h, step, 0, bad_step, 0, (1,), (0,))
    assert h(foldr(step, 0, [1])) != foldr(bad_step, 0, [1]) # 最小反例
    print("通过：融合依赖 base/step 局部等式，错误规则有最小反例。")

if __name__ == "__main__": main()

# 动手改造：证明并测试 map 后 sum 的单趟融合，记录省掉的中间列表。
