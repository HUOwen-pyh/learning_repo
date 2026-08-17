"""A small, complete DPLL solver with differential testing."""
from itertools import product
import random

def simplify(clauses, lit):
    out = []
    for clause in clauses:
        if lit in clause: continue
        reduced = tuple(x for x in clause if x != -lit)
        if not reduced: return None
        out.append(reduced)
    return tuple(out)

def verify(clauses, model):
    return all(any(model.get(abs(l),False)==(l>0) for l in c) for c in clauses)

def dpll(clauses, model=None, stats=None):
    model = {} if model is None else model
    stats = {"nodes":0} if stats is None else stats
    stats["nodes"] += 1
    if not clauses: return dict(model)
    if any(not c for c in clauses): return None
    lit = clauses[0][0]; var = abs(lit)
    if var in model:
        raise AssertionError("simplified CNF retained assigned variable")
    for value in (lit>0, lit<0):
        chosen = var if value else -var
        reduced = simplify(clauses,chosen)
        if reduced is not None:
            model[var]=value
            answer = dpll(reduced,model,stats)
            if answer is not None: return answer
            del model[var]
    return None

def brute(clauses,n):
    return next(({i+1:b for i,b in enumerate(bits)} for bits in product((False,True),repeat=n)
                 if verify(clauses,{i+1:b for i,b in enumerate(bits)})),None)

if __name__ == "__main__":
    rng=random.Random(3)
    total_nodes=0
    for _ in range(100):
        n=5
        cnf=tuple(tuple(rng.choice((-1,1))*rng.randint(1,n) for _ in range(3))
                  for _ in range(rng.randint(0,12)))
        stats={"nodes":0}; result=dpll(cnf,stats=stats); expected=brute(cnf,n)
        assert (result is None)==(expected is None)
        if result is not None: assert verify(cnf,result)
        total_nodes += stats["nodes"]
    print("100 formulas matched brute force; DPLL nodes:",total_nodes)
    # Hands-on: choose the variable with maximum occurrence and compare nodes.

