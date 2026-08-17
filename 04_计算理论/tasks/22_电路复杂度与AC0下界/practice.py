"""第22晚：小规模、低宽度 DNF 拟合 parity（实验不是下界证明）。"""
from itertools import combinations, product

def term_value(term, bits):
    # term: ((variable_index, required_bit), ...)
    return all(bits[i] == bit for i,bit in term)

def dnf_value(terms, bits):
    return any(term_value(term,bits) for term in terms)

def parity(bits):
    return sum(bits) & 1

def candidate_terms(n, max_width):
    terms = []
    for width in range(1,max_width+1):
        for variables in combinations(range(n),width):
            for signs in product((0,1),repeat=width):
                terms.append(tuple(zip(variables,signs)))
    return terms

if __name__ == "__main__":
    n, width, max_terms = 4, 2, 3
    rows = list(product((0,1),repeat=n))
    candidates = candidate_terms(n,width)
    best = (len(rows)+1,None)
    # 穷举至多3项；规模只为建立直觉。
    for k in range(max_terms+1):
        for chosen in combinations(candidates,k):
            errors = sum(dnf_value(chosen,row) != parity(row) for row in rows)
            if errors < best[0]:
                best = (errors,chosen)
    print(f"n={n}, width<={width}, terms<={max_terms}: best errors={best[0]}/{len(rows)}")
    print("best DNF terms:",best[1])
    assert 0 < best[0] < len(rows)
    # 动手改造：逐步增加宽度/项数，记录精度；不要从 n=4 外推渐近下界。
