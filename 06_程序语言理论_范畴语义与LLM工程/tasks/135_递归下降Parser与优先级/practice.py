"""表达式递归下降 parser。"""
from __future__ import annotations
import re,sys
sys.stdout.reconfigure(encoding="utf-8")

def parse(src):
    toks=re.findall(r"\d+|[()+*]",src); i=0
    def atom():
        nonlocal i
        if i>=len(toks):raise SyntaxError("expected atom")
        if toks[i].isdigit():v=("num",int(toks[i]));i+=1;return v
        if toks[i]=="(":
            i+=1;v=add()
            if i>=len(toks) or toks[i]!=")":raise SyntaxError("expected )")
            i+=1;return v
        raise SyntaxError(toks[i])
    def mul():
        nonlocal i
        v=atom()
        while i<len(toks) and toks[i]=="*":i+=1;v=("*",v,atom())
        return v
    def add():
        nonlocal i
        v=mul()
        while i<len(toks) and toks[i]=="+":i+=1;v=("+",v,mul())
        return v
    tree=add()
    if i!=len(toks):raise SyntaxError("trailing")
    return tree
def ev(t):return t[1] if t[0]=="num" else (ev(t[1])+ev(t[2]) if t[0]=="+" else ev(t[1])*ev(t[2]))

def main():
    assert ev(parse("1+2*3+4"))==11 and ev(parse("(1+2)*3"))==9
    for bad in ["","(1+2","1 2"]:
        try:parse(bad)
        except SyntaxError:pass
        else:raise AssertionError(bad)
    print(parse("1+2*3+4"))
if __name__=="__main__":main()

# 动手改造：加入右结合 ^，用 2^3^2=512 验收。
