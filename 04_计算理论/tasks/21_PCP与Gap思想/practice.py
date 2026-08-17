"""第21晚：BLR 三查询线性性检验。"""
from itertools import product
import random

def linear_table(n, mask):
    return [((x & mask).bit_count() & 1) for x in range(1 << n)]

def blr_rejection_rate(table, trials, rng):
    npoints = len(table)
    rejected = 0
    for _ in range(trials):
        x, y = rng.randrange(npoints), rng.randrange(npoints)
        rejected += table[x] ^ table[y] ^ table[x ^ y]
    return rejected / trials

def distance_to_nearest_linear(table):
    n = (len(table)-1).bit_length()
    return min(sum(a != b for a,b in zip(table,linear_table(n,mask)))
               for mask in range(1 << n)) / len(table)

if __name__ == "__main__":
    n = 6
    clean = linear_table(n,0b101011)
    rng = random.Random(21)
    assert blr_rejection_rate(clean,2000,rng) == 0
    noisy = clean[:]
    flipped = rng.sample(range(1<<n), k=10)
    for i in flipped:
        noisy[i] ^= 1
    rejection = blr_rejection_rate(noisy,10000,rng)
    distance = distance_to_nearest_linear(noisy)
    print(f"flipped={len(flipped)}/{1<<n}, nearest distance={distance:.3f}, "
          f"BLR rejection={rejection:.3f}")
    assert distance > 0 and rejection > 0
    # 动手改造：对 0%、5%、10%…噪声各重复 20 次，报告均值而非单次样本。

