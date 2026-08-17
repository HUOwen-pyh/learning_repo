"""第10晚：有限版预算化对角实验（不是层次定理证明）。"""

def m0(x, budget):
    return (x % 2 == 0) if budget >= 1 else None

def m1(x, budget):
    return (x < 3) if budget >= x + 1 else None

def m2(x, budget):
    return True if budget >= 2 ** min(x, 20) else None

MACHINES = [m0, m1, m2]

def finite_diagonal(index, budget):
    answer = MACHINES[index](index, budget)
    if answer is None:
        return None
    return not answer

if __name__ == "__main__":
    for i, machine in enumerate(MACHINES):
        budget = 2 ** (i + 2)
        own = machine(i, budget)
        diagonal = finite_diagonal(i, budget)
        print(f"M_{i}({i})={own}, D({i})={diagonal}, budget={budget}")
        assert own is not None and diagonal == (not own)
    print("Finite demo only: the hierarchy theorem also needs universal enumeration and constructible time.")
    # 动手改造：把 m2 的所需步数提高，观察预算不足只能返回 None，不能随意翻转。
