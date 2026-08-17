"""第006晚：有限域上的全称证书与存在见证。"""
from dataclasses import dataclass
from collections.abc import Callable, Iterable
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

@dataclass(frozen=True)
class ExistsWitness:
    value: int
    evidence: str

def exists(domain: Iterable[int], predicate: Callable[[int], bool]) -> ExistsWitness | None:
    for value in domain:
        if predicate(value):
            return ExistsWitness(value, f"predicate({value}) = True")
    return None

def forall(domain: Iterable[int], predicate: Callable[[int], bool]) -> tuple[bool, int | None]:
    for value in domain:
        if not predicate(value):
            return False, value
    return True, None

def main() -> None:
    witness = exists(range(6), lambda x: x * x == 9)
    assert witness is not None and witness.value == 3       # 最小正例
    assert exists(range(3), lambda x: x < 0) is None        # 最小反例
    assert forall(range(6), lambda x: x * x >= 0) == (True, None)
    assert forall(range(4), lambda x: x < 3) == (False, 3)
    assert forall((), lambda _: False) == (True, None)       # 空域边界
    assert exists((), lambda _: True) is None
    print("通过：存在交付见证；全称失败交付反例，结论限定于给定域。")

if __name__ == "__main__":
    main()

# 动手改造：为 forall 成功结果保存逐元素证据，而不只返回 True。
