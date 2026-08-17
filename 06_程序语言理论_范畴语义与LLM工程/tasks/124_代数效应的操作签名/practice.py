"""自由 effect AST：请求尚未被解释。"""
from __future__ import annotations
from dataclasses import dataclass
import sys
sys.stdout.reconfigure(encoding="utf-8")

@dataclass(frozen=True)
class Pure: value: object
@dataclass(frozen=True)
class Op: name:str; arg:object; k:object

def bind(comp,f):
    if isinstance(comp,Pure): return f(comp.value)
    if isinstance(comp,Op): return Op(comp.name,comp.arg,lambda x:bind(comp.k(x),f))
    raise TypeError(comp)

def main() -> None:
    ask=Op("Ask","name?",lambda answer:Pure(answer))
    program=bind(ask,lambda name:Op("Log",name,lambda _:Pure(f"hi {name}")))
    assert isinstance(program,Op) and program.name=="Ask"
    rest=program.k("Ada")
    assert isinstance(rest,Op) and rest.name=="Log"
    assert rest.k(None)==Pure("hi Ada")
    print("自由操作树已构造，尚未选择 handler")

if __name__ == "__main__": main()

# 动手改造：加入 ToolCall(Request→Response)，让 continuation 按响应状态分支。
