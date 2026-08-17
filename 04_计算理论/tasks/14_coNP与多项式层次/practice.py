"""第14晚：量词前缀求值，展示量词次序不可交换。"""

def eval_cnf(clauses, env):
    return all(any(env[var] == positive for var,positive in clause) for clause in clauses)

def qbf(prefix, clauses, env=None, trace=None):
    env = {} if env is None else env
    trace = [] if trace is None else trace
    if not prefix:
        value = eval_cnf(clauses, env)
        trace.append((dict(env), value))
        return value
    quantifier, var = prefix[0]
    values = []
    for bit in (False,True):
        env[var] = bit
        values.append(qbf(prefix[1:], clauses, env, trace))
    del env[var]
    return any(values) if quantifier == "E" else all(values)

if __name__ == "__main__":
    # x <-> y : (¬x∨y) ∧ (x∨¬y)
    equality = [(("x",False),("y",True)), (("x",True),("y",False))]
    trace1, trace2 = [], []
    exists_forall = qbf([("E","x"),("A","y")], equality, trace=trace1)
    forall_exists = qbf([("A","y"),("E","x")], equality, trace=trace2)
    print("exists x, forall y, x iff y:", exists_forall, "leaves:", trace1)
    print("forall y, exists x, x iff y:", forall_exists, "leaves:", trace2)
    assert not exists_forall and forall_exists
    # 动手改造：返回使 ∀ 分支失败的最短反例赋值，而不只返回布尔值。
