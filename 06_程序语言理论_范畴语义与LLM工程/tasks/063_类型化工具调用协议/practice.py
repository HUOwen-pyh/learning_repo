"""第063晚：可 replay 的类型化工具调用状态机。"""
from __future__ import annotations
from dataclasses import dataclass
import sys
if hasattr(sys.stdout,"reconfigure"):sys.stdout.reconfigure(encoding="utf-8")
@dataclass(frozen=True)
class Call:id:str;tool:str;arg:object
@dataclass(frozen=True)
class Result:id:str;value:object
@dataclass(frozen=True)
class Cancel:id:str
@dataclass(frozen=True)
class Close:pass
class ProtocolError(Exception):pass
TOOLS={"length":(str,int)}
class Machine:
    def __init__(self):self.pending=None;self.closed=False;self.trace=[]
    def apply(self,e):
        if self.closed:raise ProtocolError("closed")
        if isinstance(e,Call):
            if self.pending is not None:raise ProtocolError("already awaiting")
            if e.tool not in TOOLS or type(e.arg) is not TOOLS[e.tool][0]:raise ProtocolError("tool/schema")
            self.pending=(e.id,e.tool)
        elif isinstance(e,Result):
            if self.pending is None or e.id!=self.pending[0]:raise ProtocolError("unknown result")
            if type(e.value) is not TOOLS[self.pending[1]][1]:raise ProtocolError("result schema")
            self.pending=None
        elif isinstance(e,Cancel):
            if self.pending is None or e.id!=self.pending[0]:raise ProtocolError("unknown cancel")
            self.pending=None
        elif isinstance(e,Close):
            if self.pending is not None:raise ProtocolError("outstanding call")
            self.closed=True
        else:raise ProtocolError("event")
        self.trace.append(e)
        assert self.pending is None or isinstance(self.pending,tuple)
def replay(events):
    m=Machine()
    for e in events:m.apply(e)
    return m
def must_fail(events):
    try:replay(events)
    except ProtocolError:return
    raise AssertionError("invalid trace accepted")
def main():
    events=[Call("1","length","abc"),Result("1",3),Call("2","length","x"),Cancel("2"),Close()]
    m=replay(events);assert m.closed and m.pending is None and m.trace==events
    must_fail([Call("1","length",42)]);must_fail([Result("ghost",0)])
    must_fail([Call("1","length","a"),Result("1",1),Result("1",1)])
    must_fail([Close(),Call("x","length","late")])
    assert replay([]).pending is None
    print("第063晚通过：工具协议正常流、replay 与非法状态均已验证。")
if __name__=="__main__":main()
# 动手改造：完成 read.md 验收项中的扩展，并为新规则补一条正例和一条反例。
