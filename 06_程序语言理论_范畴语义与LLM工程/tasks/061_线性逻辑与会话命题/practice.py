"""第061晚：二方 session protocol、对偶和线性消费。"""
from __future__ import annotations
from dataclasses import dataclass
import sys
if hasattr(sys.stdout,"reconfigure"):sys.stdout.reconfigure(encoding="utf-8")
@dataclass(frozen=True)
class End:pass
@dataclass(frozen=True)
class Send:ty:type;cont:object
@dataclass(frozen=True)
class Recv:ty:type;cont:object
def dual(p):
    if isinstance(p,End):return p
    if isinstance(p,Send):return Recv(p.ty,dual(p.cont))
    if isinstance(p,Recv):return Send(p.ty,dual(p.cont))
    raise TypeError(p)
class ProtocolError(Exception):pass
class Endpoint:
    def __init__(self,p):self.p=p
    def send(self,v):
        if not isinstance(self.p,Send):raise ProtocolError("not in send state")
        if type(v) is not self.p.ty:raise ProtocolError("payload type")
        self.p=self.p.cont
    def recv(self,v):
        if not isinstance(self.p,Recv):raise ProtocolError("not in receive state")
        if type(v) is not self.p.ty:raise ProtocolError("payload type")
        self.p=self.p.cont;return v
    def close(self):
        if not isinstance(self.p,End):raise ProtocolError("protocol unfinished")
def must_fail(f):
    try:f()
    except ProtocolError:return
    raise AssertionError("protocol violation accepted")
def main():
    p=Send(str,Recv(int,End()));assert dual(dual(p))==p
    client=Endpoint(p);client.send("request");assert client.recv(200)==200;client.close()
    must_fail(lambda:Endpoint(p).recv("request"));must_fail(lambda:Endpoint(p).send(1))
    ended=Endpoint(End());ended.close();must_fail(lambda:ended.send("late"))
    print("第061晚通过：对偶可逆，方向、载荷与 End 线性约束成立。")
if __name__=="__main__":main()
# 动手改造：完成 read.md 验收项中的扩展，并为新规则补一条正例和一条反例。
