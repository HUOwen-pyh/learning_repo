"""LIFO disposer journal 与故障回滚。"""
from __future__ import annotations
import sys
sys.stdout.reconfigure(encoding="utf-8")

class Journal:
    def __init__(self): self.undo=[]
    def effect(self,do,undo): do(); self.undo.append(undo)
    def dispose(self):
        while self.undo:self.undo.pop()()

def mount(state,fail=False):
    j=Journal()
    try:
        j.effect(lambda:state.append("service"),lambda:state.remove("service"))
        j.effect(lambda:state.append("listener"),lambda:state.remove("listener"))
        if fail: raise RuntimeError("mount")
        return j
    except Exception:
        j.dispose(); raise

def main() -> None:
    state=[]; j=mount(state); assert state==["service","listener"]
    j.dispose(); assert state==[]
    try: mount(state,True)
    except RuntimeError: pass
    assert state==[]
    print("正常卸载与中途失败均无残留")

if __name__ == "__main__": main()

# 动手改造：让 listener 的 undo 断言 service 仍存在，证明 LIFO 顺序必要。
