"""有限窗口上的 Comonad 直觉模型。"""
from __future__ import annotations
from dataclasses import dataclass
import sys
sys.stdout.reconfigure(encoding="utf-8")

@dataclass(frozen=True)
class Window:
    values:tuple[int,...]
    focus:int
    def extract(self): return self.values[self.focus]

def extend(w,local):
    return Window(tuple(local(Window(w.values,i)) for i in range(len(w.values))),w.focus)

def main() -> None:
    w=Window((1,2,8),1)
    assert extend(w,Window.extract)==w
    avg=lambda x:sum(x.values)/len(x.values)
    assert extend(w,avg).extract()==11/3
    try: Window((),0).extract()
    except IndexError: pass
    else: raise AssertionError
    print("窗口 extract/extend 恒等实例通过")

if __name__ == "__main__": main()

# 动手改造：只允许半径 r 的局部视图，并把 r 作为显式 index 检查。
