"""一个单对象幺半群范畴上的 Yoneda 核心构造。"""
from __future__ import annotations
import sys
sys.stdout.reconfigure(encoding="utf-8")

MOD=4
def act(m:int,x:int)->int: return (m+x)%MOD

def from_element(x:int):
    return lambda morphism: act(morphism,x)

def to_element(alpha): return alpha(0)  # 0 是恒等态射

def main() -> None:
    for x in range(MOD):
        alpha=from_element(x)
        assert to_element(alpha)==x
        rebuilt=from_element(to_element(alpha))
        assert all(rebuilt(m)==alpha(m) for m in range(MOD))
        assert all(alpha((a+b)%MOD)==act(a,alpha(b)) for a in range(MOD) for b in range(MOD))
    print("有限作用模型中的 Yoneda 往返通过")

if __name__ == "__main__": main()

# 动手改造：换成 Z5 作用，并构造一个不满足自然性的任意分量族。
