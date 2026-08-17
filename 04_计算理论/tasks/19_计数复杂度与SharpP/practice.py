"""第19晚：#SAT 与 0-1 permanent。"""
from functools import lru_cache
from itertools import product, permutations

def simplify(clauses, var, value):
    satisfied_lit = var if value else -var
    falsified_lit = -satisfied_lit
    out = []
    for clause in clauses:
        if satisfied_lit in clause:
            continue
        reduced = tuple(lit for lit in clause if lit != falsified_lit)
        if not reduced:
            return None
        out.append(reduced)
    return tuple(out)

def count_sat(clauses, nvars):
    clauses = tuple(tuple(c) for c in clauses)
    @lru_cache(None)
    def visit(current, var):
        if not current:
            return 1 << (nvars-var+1)
        if var > nvars:
            return 0
        total = 0
        for value in (False,True):
            reduced = simplify(current,var,value)
            if reduced is not None:
                total += visit(reduced,var+1)
        return total
    result = visit(clauses,1)
    return result, visit.cache_info()

def brute_count(clauses,nvars):
    return sum(all(any(bits[abs(l)-1] == (l>0) for l in c) for c in clauses)
               for bits in product((False,True),repeat=nvars))

def permanent_ryser(matrix):
    n = len(matrix)
    total = 0
    for mask in range(1,1<<n):
        bits = mask.bit_count()
        product_rows = 1
        for row in matrix:
            product_rows *= sum(row[j] for j in range(n) if mask>>j & 1)
        total += (-1)**(n-bits) * product_rows
    return total if n else 1

def permanent_brute(matrix):
    return sum(all(matrix[i][p[i]] for i in range(len(matrix)))
               for p in permutations(range(len(matrix))))

if __name__ == "__main__":
    cnf = [(1,2),(-1,3),(2,-3)]
    count, info = count_sat(cnf,3)
    print("#SAT:",count,"cache:",info)
    assert count == brute_count(cnf,3)
    matrix = [[1,1,0],[1,0,1],[0,1,1]]
    print("perfect matchings:",permanent_ryser(matrix))
    assert permanent_ryser(matrix) == permanent_brute(matrix) == 2
    # 动手改造：增加单位传播，比较缓存状态数，但必须保持精确计数。

