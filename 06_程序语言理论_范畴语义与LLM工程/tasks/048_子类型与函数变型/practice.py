"""第 048 晚：Top、名义基础关系与箭头变型。"""
from __future__ import annotations
import sys
from dataclasses import dataclass

sys.stdout.reconfigure(encoding="utf-8")
@dataclass(frozen=True)
class Top: pass
@dataclass(frozen=True)
class Atom: name:str
@dataclass(frozen=True)
class Arrow: dom:"Ty"; cod:"Ty"
Ty=Top|Atom|Arrow; TOP=Top(); PERSON=Atom("Person"); STUDENT=Atom("Student")

def subtype(s:Ty,t:Ty)->bool:
    if s==t or isinstance(t,Top): return True
    if s==STUDENT and t==PERSON: return True
    if isinstance(s,Arrow) and isinstance(t,Arrow):
        return subtype(t.dom,s.dom) and subtype(s.cod,t.cod)
    return False

wide=Arrow(PERSON,STUDENT); narrow_view=Arrow(STUDENT,PERSON)
assert subtype(wide,narrow_view)                               # 正例：逆变+协变
assert not subtype(Arrow(STUDENT,PERSON),Arrow(PERSON,PERSON)) # 反例：错误输入方向
assert subtype(STUDENT,STUDENT) and subtype(STUDENT,TOP)       # 边界：refl/Top

# 动手改造：加入 Product，验证它的两个分量都是协变，并返回使用的规则名。
print("048 通过：函数参数逆变、结果协变的方向已通过反例校准。")

