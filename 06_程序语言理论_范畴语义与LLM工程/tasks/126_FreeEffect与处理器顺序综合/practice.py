"""同一 effect trace 的事务与审计解释。"""
from __future__ import annotations
from dataclasses import dataclass
import sys
sys.stdout.reconfigure(encoding="utf-8")

@dataclass(frozen=True)
class Event: kind:str; value:object=None

PROGRAM=[Event("inc"),Event("tool","search"),Event("fail","timeout")]
def interpret(events,transactional):
    state=0; trace=[]; start=state
    for e in events:
        if e.kind=="inc": state+=1
        elif e.kind=="tool": trace.append(e.value)
        elif e.kind=="fail":
            if transactional: state,trace=start,[]
            return False,state,trace,e.value
        else: raise ValueError(e.kind)
    return True,state,trace,None

def main() -> None:
    assert interpret(PROGRAM,True)==(False,0,[],"timeout")
    assert interpret(PROGRAM,False)==(False,1,["search"],"timeout")
    assert interpret([],True)==(True,0,[],None)
    print("事务/审计 handler 的语义差异已显式化")

if __name__ == "__main__": main()

# 动手改造：增加“批准”effect；未批准时证明工具 trace 中绝不会出现调用。
