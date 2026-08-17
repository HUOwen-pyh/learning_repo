"""词法环境上的 Let 解释器。"""
from __future__ import annotations
from dataclasses import dataclass
import sys
sys.stdout.reconfigure(encoding="utf-8")
@dataclass(frozen=True)
class Num:value:int
@dataclass(frozen=True)
class Var:name:str
@dataclass(frozen=True)
class Add:a:object;b:object
@dataclass(frozen=True)
class Let:name:str;value:object;body:object
def ev(t,env):
    if isinstance(t,Num):return t.value
    if isinstance(t,Var):return env[t.name]
    if isinstance(t,Add):return ev(t.a,env)+ev(t.b,env)
    if isinstance(t,Let):return ev(t.body,{**env,t.name:ev(t.value,env)})
    raise TypeError(t)
def main():
    t=Let("x",Num(1),Add(Let("x",Num(2),Var("x")),Var("x")))
    outer={"x":9};assert ev(t,outer)==3 and outer=={"x":9}
    try:ev(Var("missing"),{})
    except KeyError:pass
    else:raise AssertionError
    print("词法遮蔽结果=3，外层环境未变")
if __name__=="__main__":main()

# 动手改造：加入函数后同时实现词法/动态作用域，寻找最小结果差异。
