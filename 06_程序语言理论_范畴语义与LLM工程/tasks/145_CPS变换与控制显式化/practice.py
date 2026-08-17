"""直接风格与 CPS 算术求值差分。"""
from __future__ import annotations
from dataclasses import dataclass
import random,sys
sys.stdout.reconfigure(encoding="utf-8")
@dataclass(frozen=True)
class N:v:int
@dataclass(frozen=True)
class Add:a:object;b:object
def direct(t):return t.v if isinstance(t,N) else direct(t.a)+direct(t.b)
def cps(t,k):
    if isinstance(t,N):return k(t.v)
    return cps(t.a,lambda a:cps(t.b,lambda b:k(a+b)))
def gen(r,d):return N(r.randrange(8)) if d==0 else Add(gen(r,d-1),gen(r,d-1))
def safe_div(a,b,ok,err):return err("zero") if b==0 else ok(a/b)
def main():
    r=random.Random(145)
    for _ in range(100):
        t=gen(r,3);assert cps(t,lambda x:x)==direct(t)
    seen=[];assert safe_div(4,0,lambda x:seen.append("ok"),lambda e:seen.append(e)) is None
    assert seen==["zero"]
    print("CPS differential 与 error continuation 通过")
if __name__=="__main__":main()

# 动手改造：加入 Mul，并把高阶 continuation defunctionalize 成 frame 数据。
