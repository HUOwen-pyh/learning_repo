"""第16晚：QBF DFS 与存在玩家的条件策略。"""

def eval_cnf(clauses, env):
    return all(any(env[name] == sign for name,sign in c) for c in clauses)

def solve_qbf(prefix, clauses, env=None, stats=None):
    env = {} if env is None else env
    stats = {"nodes":0,"peak":0} if stats is None else stats
    stats["nodes"] += 1
    stats["peak"] = max(stats["peak"], len(env))
    if not prefix:
        return eval_cnf(clauses,env), {}
    quantifier, var = prefix[0]
    branches = []
    for bit in (False,True):
        env[var] = bit
        ok, strategy = solve_qbf(prefix[1:],clauses,env,stats)
        context = tuple(sorted((k,v) for k,v in env.items() if k != var))
        del env[var]
        branches.append((bit,ok,strategy,context))
        if quantifier == "E" and ok:
            merged = dict(strategy)
            merged[(var,context)] = bit
            return True, merged
        if quantifier == "A" and not ok:
            return False, {}
    if quantifier == "E":
        return False, {}
    merged = {}
    for _,_,strategy,_ in branches:
        merged.update(strategy)
    return True, merged

if __name__ == "__main__":
    equality = [(("x",False),("y",True)), (("x",True),("y",False))]
    stats = {"nodes":0,"peak":0}
    truth, strategy = solve_qbf([("A","y"),("E","x")],equality,stats=stats)
    print("truth:",truth,"strategy:",strategy,"stats:",stats)
    assert truth
    chosen = {context[0][1]: bit for (var,context),bit in strategy.items() if var=="x"}
    assert chosen == {False:False, True:True}
    false_value,_ = solve_qbf([("E","x"),("A","y")],equality)
    assert not false_value
    assert stats["peak"] == 2
    # 动手改造：加入短路前后的节点数对比，确认空间仍由深度控制。

