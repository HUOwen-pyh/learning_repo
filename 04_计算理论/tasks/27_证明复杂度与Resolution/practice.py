"""第27晚：生成并独立检查一个 resolution refutation。"""
from itertools import combinations

def resolvent(a,b,pivot):
    if pivot not in a or -pivot not in b:
        return None
    out = (set(a)-{pivot}) | (set(b)-{-pivot})
    if any(-lit in out for lit in out):
        return None
    return frozenset(out)

def resolution_refutation(initial):
    known = set(initial)
    records = {c:None for c in initial}
    generated = []
    while frozenset() not in known:
        changed = False
        snapshot = list(known)
        for a,b in combinations(snapshot,2):
            for pivot in a:
                r = resolvent(a,b,pivot)
                parents = (a,b,pivot)
                if r is None:
                    r = resolvent(b,a,-pivot)
                    parents = (b,a,-pivot)
                if r is not None and r not in known:
                    known.add(r); records[r]=parents; generated.append(r); changed=True
                    if not r:
                        break
            if frozenset() in known: break
        if not changed:
            return None
    needed = set()
    def collect(c):
        if c in needed: return
        needed.add(c)
        rec = records[c]
        if rec:
            collect(rec[0]); collect(rec[1])
    collect(frozenset())
    steps = [(c,records[c]) for c in generated if c in needed]
    return steps

def verify(initial,steps):
    known = set(initial)
    for clause,(a,b,pivot) in steps:
        if a not in known or b not in known or resolvent(a,b,pivot) != clause:
            return False
        known.add(clause)
    return frozenset() in known

def pigeonhole(pigeons,holes):
    var = lambda p,h: 1+p*holes+h
    clauses = [frozenset(var(p,h) for h in range(holes)) for p in range(pigeons)]
    clauses += [frozenset((-var(p,h),-var(q,h)))
                for h in range(holes) for p,q in combinations(range(pigeons),2)]
    return clauses

if __name__ == "__main__":
    cnf = pigeonhole(3,2)
    proof = resolution_refutation(cnf)
    assert proof is not None and verify(cnf,proof)
    widths = [len(c) for c,_ in proof]
    print(f"PHP(3,2): initial={len(cnf)}, proof steps={len(proof)}, max width={max(widths)}")
    broken = proof[:]
    c,(a,b,p) = broken[-1]
    broken[-1] = (c,(a,b,999))
    assert not verify(cnf,broken)
    # 动手改造：记录每个子句的父节点，打印从空子句向初始子句的 DAG。

