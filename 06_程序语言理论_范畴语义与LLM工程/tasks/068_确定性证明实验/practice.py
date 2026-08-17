"""第068晚：枚举规则候选，实验关系确定性。"""
from __future__ import annotations
from dataclasses import dataclass
import sys
if hasattr(sys.stdout,"reconfigure"):sys.stdout.reconfigure(encoding="utf-8")
@dataclass(frozen=True)
class Num:value:int
@dataclass(frozen=True)
class Add:left:object;right:object
def candidates(e,ambiguous=False):
    out=[]
    if isinstance(e,Add):
        if not isinstance(e.left,Num):
            for n in candidates(e.left,ambiguous):out.append(("ST_Add1",Add(n[1],e.right)))
        elif not isinstance(e.right,Num):
            for n in candidates(e.right,ambiguous):out.append(("ST_Add2",Add(e.left,n[1])))
        else:
            out.append(("ST_AddConst",Num(e.left.value+e.right.value)))
            if ambiguous:out.append(("BAD_Zero",Num(0)))
    return out
def deterministic(terms,ambiguous=False):
    return all(len({n for _,n in candidates(t,ambiguous)})<=1 for t in terms)
def main():
    terms=[Num(0),Add(Num(1),Num(2)),Add(Add(Num(1),Num(2)),Num(3))]
    assert deterministic(terms)
    assert candidates(Num(0))==[]                         # boundary
    witness=Add(Num(1),Num(2))
    assert not deterministic([witness],ambiguous=True)
    assert len({n for _,n in candidates(witness,True)})==2
    print("第068晚通过：标准规则确定；重叠规则给出最小非确定反例。")
if __name__=="__main__":main()
# 动手改造：完成 read.md 验收项中的扩展，并为新规则补一条正例和一条反例。
