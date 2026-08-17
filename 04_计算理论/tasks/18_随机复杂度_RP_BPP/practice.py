"""第18晚：单边误差、强伪素数见证与放大。"""
from math import gcd
import random

def strong_pass(n, a):
    if gcd(a,n) != 1:
        return False
    d, s = n-1, 0
    while d % 2 == 0:
        s += 1; d //= 2
    x = pow(a,d,n)
    if x in (1,n-1):
        return True
    for _ in range(s-1):
        x = x*x % n
        if x == n-1:
            return True
    return False

def repeated_probable_prime(n, rounds, rng):
    return all(strong_pass(n,rng.randrange(2,n-1)) for _ in range(rounds))

if __name__ == "__main__":
    for prime in [5,7,11,101]:
        assert all(strong_pass(prime,a) for a in range(2,prime-1))
    composite = 561
    bases = list(range(2,composite-1))
    liars = [a for a in bases if strong_pass(composite,a)]
    fraction = len(liars)/len(bases)
    print(f"n={composite}: liar bases={len(liars)}/{len(bases)}={fraction:.4f}")
    assert 0 < fraction < .25
    rng = random.Random(180)
    trials = 5000
    for rounds in [1,2,3]:
        errors = sum(repeated_probable_prime(composite,rounds,rng) for _ in range(trials))
        print(f"rounds={rounds}, empirical false-positive={errors/trials:.5f}, exact={fraction**rounds:.5f}")
    # 动手改造：比较“每轮重采样”和“重复同一底数”，指出独立性在哪里用到。

