"""DIMACS parsing, serialization, and independent model checking."""
from dataclasses import dataclass

@dataclass(frozen=True)
class CNF:
    variables: int
    clauses: tuple[tuple[int, ...], ...]

def parse_dimacs(text: str) -> CNF:
    header = None
    tokens = []
    for raw in text.splitlines():
        line = raw.strip()
        if not line or line.startswith("c"):
            continue
        if line.startswith("p"):
            parts = line.split()
            if len(parts) != 4 or parts[:2] != ["p", "cnf"] or header is not None:
                raise ValueError("bad or repeated header")
            header = (int(parts[2]), int(parts[3]))
        else:
            tokens.extend(map(int, line.split()))
    if header is None:
        raise ValueError("missing header")
    nvars, declared = header
    clauses, current = [], []
    for token in tokens:
        if token == 0:
            clauses.append(tuple(current)); current = []
        elif abs(token) > nvars:
            raise ValueError("variable exceeds declaration")
        else:
            current.append(token)
    if current:
        raise ValueError("unterminated clause")
    if len(clauses) != declared:
        raise ValueError("clause count mismatch")
    return CNF(nvars, tuple(clauses))

def dump_dimacs(cnf: CNF) -> str:
    body = "\n".join(" ".join(map(str, clause)) + (" " if clause else "") + "0"
                     for clause in cnf.clauses)
    return f"p cnf {cnf.variables} {len(cnf.clauses)}\n{body}\n"

def satisfies(cnf: CNF, model: dict[int, bool]) -> bool:
    return all(any(model.get(abs(lit), False) == (lit > 0) for lit in clause)
               for clause in cnf.clauses)

if __name__ == "__main__":
    text = """c demo
p cnf 3 3
1 -2 0
2 3 0
-1 -3 0
"""
    cnf = parse_dimacs(text)
    model = {1: True, 2: True, 3: False}
    print("parsed:", cnf, "model valid:", satisfies(cnf, model))
    assert satisfies(cnf, model)
    assert parse_dimacs(dump_dimacs(cnf)) == cnf
    assert satisfies(CNF(0, ()), {})
    assert not satisfies(CNF(0, ((),)), {})
    for bad in ["p cnf 1 1\n2 0\n", "p cnf 1 1\n1\n"]:
        try: parse_dimacs(bad)
        except ValueError: pass
        else: raise AssertionError("invalid DIMACS accepted")
    # Hands-on: preserve comment/source metadata in a separate return value.

