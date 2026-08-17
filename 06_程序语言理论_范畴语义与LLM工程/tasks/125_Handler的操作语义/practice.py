"""同一 effect AST 的执行与追踪 handler。"""
from __future__ import annotations
from dataclasses import dataclass
import sys
sys.stdout.reconfigure(encoding="utf-8")

@dataclass(frozen=True)
class Pure: value:object
@dataclass(frozen=True)
class Op: name:str; arg:object; k:object

def run(comp,state,trace):
    if isinstance(comp,Pure): return comp.value,state,trace
    if comp.name=="Get": return run(comp.k(state),state,trace+["Get"])
    if comp.name=="Put": return run(comp.k(None),comp.arg,trace+[f"Put({comp.arg})"])
    raise ValueError(f"unhandled:{comp.name}")

def main() -> None:
    p=Op("Get",None,lambda x:Op("Put",x+1,lambda _:Op("Get",None,lambda y:Pure(y))))
    assert run(p,4,[])==(5,5,["Get","Put(5)","Get"])
    try: run(Op("Tool",{},lambda x:Pure(x)),0,[])
    except ValueError as e: assert "unhandled" in str(e)
    else: raise AssertionError
    print("State handler 与 trace:",run(p,4,[]))

if __name__ == "__main__": main()

# 动手改造：另写一个 handler 拒绝 Put>10，并证明拒绝后 continuation 未执行。
