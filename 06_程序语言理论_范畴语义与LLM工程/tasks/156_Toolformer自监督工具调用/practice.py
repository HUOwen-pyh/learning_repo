"""Toolformer 式损失收益过滤。"""
from dataclasses import dataclass


@dataclass(frozen=True)
class Candidate:
    call: str
    loss_without: float
    loss_with: float

    @property
    def gain(self) -> float:
        return self.loss_without - self.loss_with


def select(items: list[Candidate], threshold: float) -> list[str]:
    return [x.call for x in items if x.gain > threshold]


def self_test() -> None:
    items = [Candidate("calc(2+2)", 4.0, 1.0), Candidate("noise()", 2.0, 3.0)]
    assert select(items, 1.0) == ["calc(2+2)"]                 # 正例
    assert select(items, 4.0) == []                             # 反例
    assert select([Candidate("edge", 2.0, 1.0)], 1.0) == []    # 边界：严格大于


if __name__ == "__main__":
    self_test()
    print("156 ok: hands-on: add minimum absolute quality as a second filter")
