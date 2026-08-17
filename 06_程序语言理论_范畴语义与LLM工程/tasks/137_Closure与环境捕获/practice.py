"""Closure 必须捕获定义时环境。"""
from __future__ import annotations
from dataclasses import dataclass
import sys
sys.stdout.reconfigure(encoding="utf-8")
@dataclass(frozen=True)
class Var:name:str
@dataclass(frozen=True)
class Num:value:int
@dataclass(frozen=True)
class Add:a:object;b:object
@dataclass(frozen=True)
class Lam:param:str;body:object
@dataclass(frozen=True)
class App:fn:object;arg:object
@dataclass(frozen=True)
class Closure:param:str;body:object;env:dict
def ev(t,env):
    if isinstance(t,Num):return t.value
    if isinstance(t,Var):return env[t.name]
    if isinstance(t,Add):return ev(t.a,env)+ev(t.b,env)
    if isinstance(t,Lam):return Closure(t.param,t.body,dict(env))
    if isinstance(t,App):
        c=ev(t.fn,env);v=ev(t.arg,env);return ev(c.body,{**c.env,c.param:v})
    raise TypeError
def main():
    f=ev(Lam("y",Add(Var("x"),Var("y"))),{"x":1})
    assert ev(App(Var("f"),Num(2)),{"f":f,"x":100})==3
    assert f.env=={"x":1}
    print("closure 捕获定义环境，结果=3")
if __name__=="__main__":main()

# 动手改造：实现动态作用域版本并断言同一程序结果为102。
