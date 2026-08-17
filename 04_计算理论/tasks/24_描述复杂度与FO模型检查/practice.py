"""第24晚：有限图上的一阶逻辑解释器。"""

def evaluate(formula, domain, edge, env=None):
    env = {} if env is None else env
    op = formula[0]
    if op == "edge":
        return (env[formula[1]],env[formula[2]]) in edge
    if op == "eq":
        return env[formula[1]] == env[formula[2]]
    if op == "not":
        return not evaluate(formula[1],domain,edge,env)
    if op == "and":
        return all(evaluate(f,domain,edge,env) for f in formula[1:])
    if op == "or":
        return any(evaluate(f,domain,edge,env) for f in formula[1:])
    if op in ("exists","forall"):
        var, body = formula[1], formula[2]
        old = env.get(var,None); had = var in env
        values = []
        for value in domain:
            env[var] = value
            values.append(evaluate(body,domain,edge,env))
        if had: env[var] = old
        else: env.pop(var,None)
        return any(values) if op == "exists" else all(values)
    raise ValueError(op)

def undirected(pairs):
    return {(u,v) for u,v in pairs} | {(v,u) for u,v in pairs}

if __name__ == "__main__":
    distinct3 = ("and",("not",("eq","x","y")),("not",("eq","x","z")),
                 ("not",("eq","y","z")))
    triangle = ("exists","x",("exists","y",("exists","z",
                ("and",distinct3,("edge","x","y"),("edge","y","z"),("edge","z","x")))))
    no_isolated = ("forall","x",("exists","y",("edge","x","y")))
    g1 = undirected({(0,1),(1,2),(2,0)})
    g2 = undirected({(0,1),(1,2)})
    assert evaluate(triangle,range(3),g1)
    assert not evaluate(triangle,range(3),g2)
    assert evaluate(no_isolated,range(3),g1)
    print("triangle/no-isolated:",[(evaluate(triangle,range(3),g),evaluate(no_isolated,range(3),g))
                                   for g in (g1,g2)])
    # 动手改造：增加关系谓词 label(x)，表达“存在带标签的三角形”。

