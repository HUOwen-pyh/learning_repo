"""第 049 晚：记录子类型驱动的最小 schema checker。"""
from __future__ import annotations
import sys
from dataclasses import dataclass

sys.stdout.reconfigure(encoding="utf-8")
@dataclass(frozen=True)
class Top: pass
@dataclass(frozen=True)
class Atom: name:str
@dataclass(frozen=True)
class RecordTy: fields:tuple[tuple[str,"Ty"],...]
Ty=Top|Atom|RecordTy; TOP=Top(); STRING=Atom("String"); NAT=Atom("Nat")
PERSON=RecordTy((("name",STRING),("age",NAT)))
STUDENT=RecordTy((("name",STRING),("age",NAT),("gpa",NAT)))

def field_map(r:RecordTy)->dict[str,Ty]:
    out=dict(r.fields)
    if len(out)!=len(r.fields): raise ValueError("重复 label")
    return out
def subtype(s:Ty,t:Ty)->bool:
    if s==t or isinstance(t,Top): return True
    if isinstance(s,RecordTy) and isinstance(t,RecordTy):
        sf,tf=field_map(s),field_map(t)
        return all(k in sf and subtype(sf[k],ty) for k,ty in tf.items())
    return False
@dataclass(frozen=True)
class RecordV: fields:tuple[tuple[str,object],...]
def infer_value(value:object)->Ty:
    if isinstance(value,str): return STRING
    if type(value) is int and value>=0: return NAT
    if isinstance(value,RecordV): return infer(value)
    raise TypeError(f"无 schema 类型的 payload: {value!r}")
def infer(v:RecordV)->RecordTy:
    labels=[k for k,_ in v.fields]
    if len(labels)!=len(set(labels)): raise ValueError("重复字段")
    return RecordTy(tuple((k,infer_value(value)) for k,value in v.fields))
def check_as(v:RecordV,expected:RecordTy)->bool:
    return subtype(infer(v),expected)

alice=RecordV((("gpa",4),("name","Alice"),("age",20)))
assert check_as(alice,PERSON) and subtype(STUDENT,PERSON)        # 正例/排列
missing=RecordV((("name","Bob"),))
assert not check_as(missing,PERSON)                             # 反例：缺字段
assert subtype(RecordTy(()),RecordTy(()))                       # 边界：空记录
assert not check_as(RecordV((("name","Eve"),("age","twenty"))),PERSON)
try: check_as(RecordV((("name","Eve"),("age",True))),PERSON)
except TypeError: pass                                          # bool 不能冒充 Nat
else: raise AssertionError("应拒绝没有 schema 类型的 payload")

# 动手改造：返回缺失/错型/多余字段三份诊断，并让多余字段只告警、不失败。
print("049 通过：富记录可忘却额外字段，缺失必需字段会被拒绝。")
