"""第13晚：随机对拍 3SAT -> CLIQUE 归约。"""
from itertools import combinations, product
import random

def eval_formula(formula, assignment):
    return all(any(assignment[abs(x)] == (x > 0) for x in clause) for clause in formula)

def brute_sat(formula, n):
    for bits in product((False,True), repeat=n):
        if eval_formula(formula, {i+1:b for i,b in enumerate(bits)}):
            return True
    return False

def reduce_to_clique(formula):
    vertices = [(ci, pos, lit) for ci,c in enumerate(formula) for pos,lit in enumerate(c)]
    edges = {frozenset((u,v)) for u,v in combinations(vertices,2)
             if u[0] != v[0] and u[2] != -v[2]}
    return vertices, edges

def has_clique(vertices, edges, k):
    return any(all(frozenset((u,v)) in edges for u,v in combinations(group,2))
               for group in combinations(vertices,k))

if __name__ == "__main__":
    rng = random.Random(20260813)
    tested = 0
    for _ in range(100):
        n, m = 4, 4
        formula = [tuple(rng.choice((-1,1))*rng.randint(1,n) for _ in range(3))
                   for _ in range(m)]
        vertices, edges = reduce_to_clique(formula)
        assert brute_sat(formula,n) == has_clique(vertices,edges,m), formula
        tested += 1
    print(f"{tested} random reductions preserved YES and NO.")
    # 动手改造：实现长子句到 3CNF 的辅助变量链，并继续随机对拍。

