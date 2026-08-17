"""带显式块的 toy CFG verifier。"""
from __future__ import annotations
import sys
sys.stdout.reconfigure(encoding="utf-8")
TERMS={"JMP","JZ","RET"}
def cfg(blocks):
    edges={k:set() for k in blocks}
    for name,code in blocks.items():
        if not code or code[-1][0] not in TERMS:raise ValueError(f"no terminator:{name}")
        op,*args=code[-1]
        targets=args if op in {"JMP","JZ"} else []
        if any(t not in blocks for t in targets):raise ValueError("unknown target")
        edges[name].update(targets)
    seen=set();todo=["entry"]
    while todo:
        n=todo.pop()
        if n not in seen:seen.add(n);todo.extend(edges[n]-seen)
    return edges,set(blocks)-seen
def main():
    b={"entry":[("JZ","then","else")],"then":[("JMP","join")],"else":[("JMP","join")],"join":[("RET",)],"dead":[("RET",)]}
    e,dead=cfg(b);assert e["entry"]=={"then","else"} and dead=={"dead"}
    try:cfg({"entry":[("JMP","missing")]})
    except ValueError:pass
    else:raise AssertionError
    print("CFG=",e,"unreachable=",dead)
if __name__=="__main__":main()

# 动手改造：计算每块 dominator 集，验证 join 被 entry 支配。
