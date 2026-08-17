"""第28晚：一量子比特 Deutsch 相位算法。"""
from math import sqrt
import random

H = ((1/sqrt(2),1/sqrt(2)),(1/sqrt(2),-1/sqrt(2)))

def apply_gate(state,gate):
    return [gate[0][0]*state[0]+gate[0][1]*state[1],
            gate[1][0]*state[0]+gate[1][1]*state[1]]

def phase_oracle(state,function):
    return [amplitude*((-1)**function(x)) for x,amplitude in enumerate(state)]

def norm2(state):
    return sum(abs(a)**2 for a in state)

def deutsch(function):
    state = [1+0j,0j]
    state = apply_gate(state,H)
    assert abs(norm2(state)-1)<1e-12
    state = phase_oracle(state,function)
    state = apply_gate(state,H)
    probabilities = [abs(a)**2 for a in state]
    return probabilities

def sample(probabilities,rng):
    return 0 if rng.random()<probabilities[0] else 1

if __name__ == "__main__":
    functions = {
        "constant-0":lambda x:0, "constant-1":lambda x:1,
        "balanced-x":lambda x:x, "balanced-not-x":lambda x:1-x,
    }
    rng = random.Random(28)
    for name,function in functions.items():
        probabilities = deutsch(function)
        observations = [sample(probabilities,rng) for _ in range(20)]
        expected = 0 if name.startswith("constant") else 1
        print(name,probabilities,observations[:5])
        assert observations == [expected]*20
        assert abs(sum(probabilities)-1)<1e-12
    # 动手改造：实现二量子比特张量态和单比特 H，逐门检查归一化。

