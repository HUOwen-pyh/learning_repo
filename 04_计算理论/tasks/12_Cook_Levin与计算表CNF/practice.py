"""第12晚：把微型非确定计算历史编码成 CNF。"""
from itertools import product

def exactly_one(variables):
    return [tuple(variables)] + [(-a,-b) for i,a in enumerate(variables) for b in variables[i+1:]]

def tableau_cnf(input_bit):
    states = ("S","g0","g1","A","R")
    times = range(3)
    vid = {(t,q): 1 + t*len(states) + i for t in times for i,q in enumerate(states)}
    clauses = []
    for t in times:
        clauses += exactly_one([vid[(t,q)] for q in states])
    clauses += [(vid[(0,"S")],), (vid[(2,"A")],)]
    allowed0 = {("S","g0"), ("S","g1")}
    allowed1 = {
        ("g0", "A" if (0 ^ input_bit) == 1 else "R"),
        ("g1", "A" if (1 ^ input_bit) == 1 else "R"),
    }
    for t, allowed in [(0,allowed0), (1,allowed1)]:
        for q in states:
            for r in states:
                if (q,r) not in allowed:
                    clauses.append((-vid[(t,q)], -vid[(t+1,r)]))
    return clauses, vid, states

def satisfies(clauses, bits):
    return all(any(bits[abs(lit)-1] == (lit > 0) for lit in clause) for clause in clauses)

def solve(clauses, nvars):
    for bits in product((False,True), repeat=nvars):
        if satisfies(clauses, bits):
            return bits
    return None

def decode(model, vid, states):
    return [next(q for q in states if model[vid[(t,q)]-1]) for t in range(3)]

if __name__ == "__main__":
    for bit in (0,1):
        cnf, vid, states = tableau_cnf(bit)
        model = solve(cnf, len(vid))
        history = decode(model, vid, states)
        print(f"input={bit}, clauses={len(cnf)}, accepting history={history}")
        assert history[0] == "S" and history[-1] == "A"
        guessed = int(history[1][-1])
        assert guessed ^ bit == 1
        broken = cnf + [(-vid[(2,"A")],)]
        assert solve(broken, len(vid)) is None
    # 动手改造：给每格增加“恰有一个符号”约束，做一个 2 格纸带 tableau。

