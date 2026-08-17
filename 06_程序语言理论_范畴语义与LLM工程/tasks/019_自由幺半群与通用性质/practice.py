"""第019晚：自由幺半群映射的 fold 扩张。"""
from itertools import product
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

def extend(generator_map, op, identity):
    def hom(word):
        result = identity
        for letter in word: result = op(result, generator_map(letter))
        return result
    return hom

def words(alphabet, max_len):
    for n in range(max_len + 1):
        yield from product(alphabet, repeat=n)

def main() -> None:
    weights = {"a": 2, "b": 3}
    hom = extend(weights.__getitem__, lambda x, y: x + y, 0)
    assert hom(()) == 0                                      # 空词正例
    assert hom(("a",)) == 2 and hom(("a", "b")) == 5
    for u in words("ab", 2):
        for v in words("ab", 2):
            assert hom(u + v) == hom(u) + hom(v)             # 同态律
    bad = lambda word: 1 + hom(word)
    assert bad(()) != 0                                      # 最小反例：不保单位元
    assert all(hom((x,)) == weights[x] for x in weights)
    print("通过：生成元映射经 fold 唯一决定所有有限词的解释。")

if __name__ == "__main__": main()

# 动手改造：枚举小词，拒绝一个在长度2处偷偷偏离 fold 的候选同态。
