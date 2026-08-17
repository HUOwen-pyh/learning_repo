"""Inspect 风格但仅标准库的 Task/Solver/Scorer。"""
from dataclasses import dataclass
from typing import Callable


@dataclass(frozen=True)
class Sample:
    id: str
    prompt: str
    target: str


@dataclass(frozen=True)
class Task:
    dataset: tuple[Sample, ...]
    solver: Callable[[str], str]
    scorer: Callable[[str, str], float]


def evaluate(task: Task) -> list[tuple[str, float]]:
    return [(s.id, task.scorer(task.solver(s.prompt), s.target)) for s in task.dataset]


def self_test() -> None:
    exact = lambda got, want: float(got == want)
    task = Task((Sample("a", " hi ", "HI"),), lambda x: x.strip().upper(), exact)
    assert evaluate(task) == [("a", 1.0)]                    # 正例
    assert evaluate(Task((Sample("b", "x", "y"),), lambda x: x, exact)) == [("b", 0.0)]
    assert evaluate(Task((), str, exact)) == []               # 边界


if __name__ == "__main__":
    self_test()
    print("159 ok: hands-on: compose normalize and answer as two named solvers")
