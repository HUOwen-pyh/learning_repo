"""第090晚：二状态模型中 model validity 与 derivability 穷举。"""
from itertools import combinations
import sys
if hasattr(sys.stdout,"reconfigure"):sys.stdout.reconfigure(encoding="utf-8")
U=frozenset({0,1})
def predicates():
    xs=list(U)
    return [frozenset(xs[i] for i in range(len(xs)) if mask>>i&1) for mask in range(1<<len(xs))]
COMMANDS={"skip":lambda x:x,"flip":lambda x:1-x,"zero":lambda x:0}
def wp(cmd,Q):return frozenset(x for x in U if cmd(x) in Q)
def sem_valid(P,cmd,Q):return all(cmd(x) in Q for x in P)
def derivable(P,cmd,Q):return P<=wp(cmd,Q)                 # complete finite assertion language
def bad_derivable(P,cmd,Q):return len(P)<=len(Q)           # unsound fake rule
def main():
    for cmd in COMMANDS.values():
        for P in predicates():
            for Q in predicates():
                assert sem_valid(P,cmd,Q)==derivable(P,cmd,Q)
    witness=next((P,c,Q) for c in COMMANDS.values() for P in predicates() for Q in predicates() if bad_derivable(P,c,Q) and not sem_valid(P,c,Q))
    assert witness
    assert derivable(frozenset(),COMMANDS["flip"],frozenset()) # vacuous boundary
    print("第090晚通过：有限模型中 soundness/completeness 双向成立，伪规则被击穿。")
if __name__=="__main__":main()
# 动手改造：完成 read.md 验收项中的扩展，并为新规则补一条正例和一条反例。
