"""Result 的 Kleisli 复合。"""
from __future__ import annotations
from dataclasses import dataclass
import sys
sys.stdout.reconfigure(encoding="utf-8")

@dataclass(frozen=True)
class Ok: value: object
@dataclass(frozen=True)
class Err: message: str
def bind(r,f): return f(r.value) if isinstance(r,Ok) else r
def kleisli(f,g): return lambda x:bind(f(x),g)
def parse(s):
    try:return Ok(int(s))
    except ValueError:return Err("not-int")
def positive(x): return Ok(x) if x>0 else Err("non-positive")
def reciprocal(x): return Ok(1/x)

def main() -> None:
    pipe=kleisli(kleisli(parse,positive),reciprocal)
    assert pipe("4")==Ok(.25)
    assert pipe("0")==Err("non-positive") and pipe("x")==Err("not-int")
    left=kleisli(kleisli(parse,positive),reciprocal)
    right=kleisli(parse,kleisli(positive,reciprocal))
    assert all(left(x)==right(x) for x in ["2","0","x"])
    print("Result Kleisli 的短路与结合律通过")

if __name__ == "__main__": main()

# 动手改造：加入最大值校验，比较重新括号化前后的错误信息。
