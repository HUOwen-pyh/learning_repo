"""Linear Tseitin encoding, checked by exhaustive projection."""
from itertools import product

class Encoder:
    def __init__(self, original_vars):
        self.next_var = original_vars + 1
        self.clauses = []
    def fresh(self):
        v = self.next_var; self.next_var += 1; return v
    def gate_not(self, x):
        z = self.fresh()
        self.clauses += [(-z,-x),(z,x)]
        return z
    def gate_and(self, x, y):
        z = self.fresh()
        self.clauses += [(-z,x),(-z,y),(z,-x,-y)]
        return z
    def gate_or(self, x, y):
        z = self.fresh()
        self.clauses += [(z,-x),(z,-y),(-z,x,y)]
        return z

def sat_extensions(clauses, fixed, nvars):
    free = [v for v in range(1,nvars+1) if v not in fixed]
    for bits in product((False,True), repeat=len(free)):
        model = dict(fixed); model.update(zip(free,bits))
        if all(any(model[abs(l)] == (l>0) for l in c) for c in clauses):
            yield model

def expression(a,b,c):
    return (a and b) or (not c)

if __name__ == "__main__":
    enc = Encoder(3)
    ab = enc.gate_and(1,2)
    nc = enc.gate_not(3)
    root = enc.gate_or(ab,nc)
    enc.clauses.append((root,))
    nvars = enc.next_var-1
    for a,b,c in product((False,True), repeat=3):
        fixed = {1:a,2:b,3:c}
        extensions = list(sat_extensions(enc.clauses,fixed,nvars))
        assert bool(extensions) == expression(a,b,c)
        assert len(extensions) <= 1  # functional gate definitions
    print(f"3 original vars, {nvars-3} auxiliaries, {len(enc.clauses)} clauses")
    # Hands-on: add XOR z <-> x xor y and verify all four rows.

