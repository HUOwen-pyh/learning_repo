"""值与计算 AST 的最小类型边界。"""
from __future__ import annotations
from dataclasses import dataclass
import sys
sys.stdout.reconfigure(encoding="utf-8")

@dataclass(frozen=True)
class Value: value: int
@dataclass(frozen=True)
class Return: value: Value
@dataclass(frozen=True)
class Fail: message: str
@dataclass(frozen=True)
class Bind: comp: object; cont: object

def is_computation(x): return isinstance(x,(Return,Fail,Bind))
def bind(comp,cont):
    if not is_computation(comp): raise TypeError("bind 左侧必须是计算")
    return Bind(comp,cont)

def main() -> None:
    p=bind(Return(Value(2)),lambda x:Return(Value(x.value+1)))
    assert is_computation(p) and is_computation(Fail("x"))
    try: bind(Value(2),lambda x:Return(x))
    except TypeError: pass
    else: raise AssertionError
    print("值 A 与计算 T A 的边界已检查")

if __name__ == "__main__": main()

# 动手改造：为 AST 加结果类型标签，拒绝 continuation 输入/输出类型不匹配。
