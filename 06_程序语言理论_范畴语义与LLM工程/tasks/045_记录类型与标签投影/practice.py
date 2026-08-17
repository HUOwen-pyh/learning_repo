"""第 045 晚：有限标签映射形式的记录。"""
from __future__ import annotations
import sys
from dataclasses import dataclass

sys.stdout.reconfigure(encoding="utf-8")
@dataclass(frozen=True)
class BoolTy: pass
@dataclass(frozen=True)
class RecordTy: fields:tuple[tuple[str,"Ty"],...]
Ty=BoolTy|RecordTy; B=BoolTy()
@dataclass(frozen=True)
class Lit: value:bool
@dataclass(frozen=True)
class Record: fields:tuple[tuple[str,"T"],...]
@dataclass(frozen=True)
class Proj: record:"T"; label:str
T=Lit|Record|Proj

def ensure_unique(fields:tuple[tuple[str,object],...])->None:
    labels=[k for k,_ in fields]
    if len(labels)!=len(set(labels)): raise ValueError("重复字段")
def infer(t:T)->Ty:
    if isinstance(t,Lit): return B
    if isinstance(t,Record):
        ensure_unique(t.fields); return RecordTy(tuple((k,infer(v)) for k,v in t.fields))
    rt=infer(t.record)
    if not isinstance(rt,RecordTy): raise TypeError("只能投影记录")
    for k,ty in rt.fields:
        if k==t.label: return ty
    raise TypeError(f"缺失字段 {t.label}")
def value(t:T)->bool:
    return isinstance(t,Lit) or isinstance(t,Record) and all(value(v) for _,v in t.fields)
def step(t:T)->T|None:
    if isinstance(t,Record):
        for i,(label,field) in enumerate(t.fields):
            if not value(field):
                nxt=step(field)
                if nxt is None: return None
                fields=list(t.fields); fields[i]=(label,nxt)
                return Record(tuple(fields))
        return None
    if isinstance(t,Proj):
        if not value(t.record):
            record=step(t.record); return Proj(record,t.label) if record is not None else None
        if isinstance(t.record,Record):
            for k,v in t.record.fields:
                if k==t.label: return v
    return None

r=Record((("ok",Lit(True)),("cached",Lit(False))))
assert infer(Proj(r,"ok"))==B and step(Proj(r,"ok"))==Lit(True) # 正例
try: infer(Proj(r,"missing"))                                  # 反例
except TypeError: pass
else: raise AssertionError("应拒绝缺失字段")
assert infer(Record(()))==RecordTy(())                          # 边界：空记录
delayed=Record((("first",Proj(r,"ok")),("second",Proj(r,"cached"))))
assert step(delayed)==Record((("first",Lit(True)),("second",Proj(r,"cached"))))
assert step(Proj(delayed,"second"))==Proj(step(delayed),"second") # 未成 value 前不能提前投影

# 动手改造：规范化字段顺序，使两个排列不同的同字段记录类型可结构比较。
print("045 通过：记录标签唯一，静态与运行时投影一致。")
