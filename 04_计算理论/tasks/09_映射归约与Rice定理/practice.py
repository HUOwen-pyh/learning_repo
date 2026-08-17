"""第09晚：3CNF 到 CLIQUE 的映射归约与穷举核验。"""
from itertools import combinations, product

def eval_cnf(formula, assignment):
    return all(any(assignment[abs(lit)] == (lit > 0) for lit in clause) for clause in formula)

def sat(formula):
    n = max((abs(x) for c in formula for x in c), default=0)
    return any(eval_cnf(formula, dict(zip(range(1,n+1), bits)))
               for bits in product((False,True), repeat=n))

def cnf_to_clique(formula):
    vertices = [(i, lit) for i, clause in enumerate(formula) for lit in clause]
    edges = set()
    for u, v in combinations(vertices, 2):
        if u[0] != v[0] and u[1] != -v[1]:
            edges.add(frozenset((u,v)))
    return vertices, edges, len(formula)

def has_k_clique(vertices, edges, k):
    for chosen in combinations(vertices, k):
        if all(frozenset((u,v)) in edges for u,v in combinations(chosen,2)):
            return True, chosen
    return False, None

if __name__ == "__main__":
    samples = [
        [(1,2,3), (-1,2,-3), (1,-2,3)],
        [(1,1,1), (-1,-1,-1)],
        [],
    ]
    for formula in samples:
        vertices, edges, k = cnf_to_clique(formula)
        reduced, witness = has_k_clique(vertices, edges, k)
        original = sat(formula)
        print(formula, "SAT=", original, "clique witness=", witness)
        assert original == reduced
    # 动手改造：随机生成 100 个小 3CNF，验证 YES 与 NO 两个方向。

