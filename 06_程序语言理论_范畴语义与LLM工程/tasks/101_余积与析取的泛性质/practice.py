"""带标签余积与唯一 case 态射。"""
from __future__ import annotations
from dataclasses import dataclass
import sys
sys.stdout.reconfigure(encoding="utf-8")

@dataclass(frozen=True)
class Inl: value: int
@dataclass(frozen=True)
class Inr: value: int

def copair(f, g):
    def case(value):
        if isinstance(value, Inl): return f(value.value)
        if isinstance(value, Inr): return g(value.value)
        raise TypeError("not a coproduct value")
    return case

def main() -> None:
    h = copair(lambda x: f"left:{x}", lambda x: f"right:{x}")
    assert h(Inl(0)) == "left:0"
    assert h(Inr(0)) == "right:0"
    assert Inl(0) != Inr(0)
    try: h(0)
    except TypeError: pass
    else: raise AssertionError("裸值不应通过穷尽 case")
    print("余积标签保留了来源，case 两支可独立定义")

if __name__ == "__main__": main()

# 动手改造：加入第三个分支，并让未处理分支成为可执行失败测试。
