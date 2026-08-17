"""第26晚：指数底数、meet-in-the-middle 与条件性表述。"""
from itertools import combinations
import random

def subset_sums(values):
    sums = {0}
    for value in values:
        sums |= {s+value for s in list(sums)}
    return sums

def subset_sum_mitm(values,target):
    mid = len(values)//2
    left, right = subset_sums(values[:mid]), subset_sums(values[mid:])
    right_set = set(right)
    return any(target-x in right_set for x in left), len(left)+len(right)

def subset_sum_brute(values,target):
    operations = 0
    for r in range(len(values)+1):
        for chosen in combinations(values,r):
            operations += 1
            if sum(chosen)==target:
                return True,operations
    return False,operations

if __name__ == "__main__":
    print("theoretical operation counts")
    for n in [10,20,30,40]:
        print(f"n={n:2}: brute~{2**n:12}, MITM storage/work~{2*2**(n//2):8}")
    rng = random.Random(26)
    values = [rng.randrange(1,1000) for _ in range(18)]
    target = sum(values[::3])
    b, brute_ops = subset_sum_brute(values,target)
    m, mitm_states = subset_sum_mitm(values,target)
    print("actual found:",b,"brute candidates:",brute_ops,"MITM distinct states:",mitm_states)
    assert b == m == True
    # 动手改造：使用一个保证无解且接近总和一半的 target，避免提前命中偏差。
