"""异常/状态两种堆叠的可观察差异。"""
from __future__ import annotations
import sys
sys.stdout.reconfigure(encoding="utf-8")

def rollback_runner(initial, fail_after_update):
    new=initial+1
    return (False,"boom") if fail_after_update else (True,(new,new))
def audit_runner(initial, fail_after_update):
    new=initial+1
    return ((False,"boom"),new) if fail_after_update else ((True,new),new)

def main() -> None:
    assert rollback_runner(0,True)==(False,"boom")
    assert audit_runner(0,True)==((False,"boom"),1)
    assert rollback_runner(0,False)==(True,(1,1))
    assert audit_runner(0,False)==((True,1),1)
    print("失败后状态：rollback 丢弃，audit 保留")

if __name__ == "__main__": main()

# 动手改造：加入两次更新和第二步失败，写出事务/审计两套验收不变量。
