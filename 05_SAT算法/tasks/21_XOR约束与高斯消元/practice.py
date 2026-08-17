"""GF(2) Gaussian elimination with rank, solution, and brute checks."""
from itertools import product
import random

def solve_xor(rows,n):
    rows=[[mask,rhs&1] for mask,rhs in rows]
    pivot_row=0;pivots=[]
    for col in range(n):
        found=next((r for r in range(pivot_row,len(rows)) if rows[r][0]>>col&1),None)
        if found is None:continue
        rows[pivot_row],rows[found]=rows[found],rows[pivot_row]
        for r in range(len(rows)):
            if r!=pivot_row and rows[r][0]>>col&1:
                rows[r][0]^=rows[pivot_row][0];rows[r][1]^=rows[pivot_row][1]
        pivots.append(col);pivot_row+=1
    if any(mask==0 and rhs for mask,rhs in rows):return None,len(pivots)
    x=[0]*n
    for r,col in reversed(list(enumerate(pivots))):
        mask,rhs=rows[r]
        rhs ^= sum(x[j] for j in range(col+1,n) if mask>>j&1)&1
        x[col]=rhs
    return x,len(pivots)

def verify(rows,x):
    return all((sum(x[j] for j in range(len(x)) if mask>>j&1)&1)==rhs for mask,rhs in rows)

if __name__=="__main__":
    rng=random.Random(21)
    for _ in range(100):
        n=7;rows=[(rng.randrange(1<<n),rng.randrange(2)) for _ in range(8)]
        solution,rank=solve_xor(rows,n)
        brute=next((list(bits) for bits in product((0,1),repeat=n) if verify(rows,bits)),None)
        assert (solution is None)==(brute is None)
        if solution is not None:assert verify(rows,solution) and 0<=rank<=n
    contradiction=[(1,0),(1,1)]
    assert solve_xor(contradiction,1)[0] is None
    print("100 systems matched brute force; explicit contradiction detected.")
    # Hands-on: return a linear-combination explanation for each contradiction.

