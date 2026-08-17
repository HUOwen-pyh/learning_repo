"""第20晚：二变量 sum-check 的诚实与作弊实验。"""
import random

def poly(x,y,p):
    return (x*y + x + 2*y + 3) % p

def run_protocol(p, rng, cheat=0):
    true_sum = sum(poly(x,y,p) for x in (0,1) for y in (0,1)) % p
    def honest_g1(x):
        return (poly(x,0,p)+poly(x,1,p)) % p
    # cheat*(2x-1) 在 0/1 两端之和为0，能通过第一项和检查。
    def claimed_g1(x):
        return (honest_g1(x) + cheat*(2*x-1)) % p
    if (claimed_g1(0)+claimed_g1(1)) % p != true_sum:
        return False
    r1 = rng.randrange(p)
    def honest_g2(y):
        return poly(r1,y,p)
    if (honest_g2(0)+honest_g2(1)) % p != claimed_g1(r1):
        return False
    r2 = rng.randrange(p)
    return honest_g2(r2) == poly(r1,r2,p)

if __name__ == "__main__":
    p = 101
    rng = random.Random(2020)
    assert all(run_protocol(p,rng,cheat=0) for _ in range(1000))
    trials = 10000
    accepted = sum(run_protocol(p,rng,cheat=7) for _ in range(trials))
    rate = accepted/trials
    print(f"honest acceptance=1; cheating acceptance={rate:.4f}; degree/field~{1/p:.4f}")
    assert 0 < rate < .03
    # 动手改造：换不同素数域，作表比较经验漏检率与 1/p。
