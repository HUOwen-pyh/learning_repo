"""第30晚：SAT/#SAT/CLIQUE/证书的一体化可复现实验。"""
from itertools import product,combinations
import json,time

def verify_model(formula,model):
    return all(any(model.get(abs(lit)) == (lit>0) for lit in clause) for clause in formula)

def solve_and_count(formula):
    n=max((abs(l) for c in formula for l in c),default=0)
    count,first,nodes=0,None,0
    for bits in product((False,True),repeat=n):
        nodes+=1
        model={i+1:b for i,b in enumerate(bits)}
        if verify_model(formula,model):
            count+=1
            if first is None:first=model
    return first,count,nodes

def reduce_clique(formula):
    vertices=[(i,j,l) for i,c in enumerate(formula) for j,l in enumerate(c)]
    edges={frozenset((u,v)) for u,v in combinations(vertices,2)
           if u[0]!=v[0] and u[2]!=-v[2]}
    return vertices,edges,len(formula)

def find_clique(vertices,edges,k):
    return next((c for c in combinations(vertices,k)
                 if all(frozenset((u,v)) in edges for u,v in combinations(c,2))),None)

def verify_resolution_step(parent_a,parent_b,pivot,child):
    if pivot not in parent_a or -pivot not in parent_b:return False
    expected=(set(parent_a)-{pivot})|(set(parent_b)-{-pivot})
    return not any(-x in expected for x in expected) and frozenset(expected)==child

def experiment(name,formula):
    start=time.perf_counter()
    model,count,nodes=solve_and_count(formula)
    vertices,edges,k=reduce_clique(formula)
    clique=find_clique(vertices,edges,k)
    elapsed_ms=(time.perf_counter()-start)*1000
    assert (model is not None)==(clique is not None)
    if model is not None: assert verify_model(formula,model)
    return {"name":name,"variables":max((abs(l) for c in formula for l in c),default=0),
            "clauses":len(formula),"sat":model is not None,"models":count,
            "search_nodes":nodes,"clique_witness":clique,"elapsed_ms":round(elapsed_ms,3)}

if __name__ == "__main__":
    sat_instance=[(1,2),(-1,3),(2,-3)]
    unsat_instance=[(1,),(-1,)]
    reports=[experiment("sat-demo",sat_instance),experiment("unsat-demo",unsat_instance)]
    a,b=frozenset({1}),frozenset({-1})
    assert verify_resolution_step(a,b,1,frozenset())
    output={"seed":None,
            "labels":{"THEOREM":"3SAT maps to CLIQUE","EXPERIMENT":"small exhaustive results",
                      "OPEN":"P versus NP is unresolved"},
            "instances":reports}
    print(json.dumps(output,ensure_ascii=False,indent=2,default=list))
    assert reports[0]["sat"] and reports[0]["models"]>0
    assert not reports[1]["sat"] and reports[1]["models"]==0
    # 动手改造：加入固定种子的随机 CNF 族；把超预算结果标成 UNKNOWN。

