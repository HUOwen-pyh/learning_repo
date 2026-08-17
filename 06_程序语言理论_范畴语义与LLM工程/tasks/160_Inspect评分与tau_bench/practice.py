"""终态不变量评分与按任务、按重复试验计算的 pass^k。"""
from dataclasses import dataclass
from math import comb


@dataclass(frozen=True)
class State:
    status: str
    balance: int


def score(state: State, target: State) -> float:
    checks = (state.status == target.status, state.balance == target.balance, state.balance >= 0)
    return sum(checks) / len(checks)


def pass_power(trials_by_task: dict[str, list[bool]], k: int) -> float:
    """返回 τ-bench 的逐任务组合数无偏 pass^k 估计。

    每项为 C(c, k) / C(n, k)，其中 n 是该任务的 trial 数、c 是成功数；
    再跨任务平均。n=k 时才退化为“该任务全部 k 次成功”的 0/1 指示量。
    """
    if k < 0:
        raise ValueError("k must be non-negative")
    if k == 0:
        return 1.0
    if not trials_by_task:
        return 0.0
    if any(len(trials) < k for trials in trials_by_task.values()):
        raise ValueError("every task must have at least k trials")
    estimates = (
        comb(sum(trials), k) / comb(len(trials), k)
        for trials in trials_by_task.values()
    )
    return sum(estimates) / len(trials_by_task)


def self_test() -> None:
    assert score(State("paid", 10), State("paid", 10)) == 1.0     # 正例
    assert score(State("paid", -1), State("paid", 10)) == 1/3    # 反例
    trials = {
        "task-a": [True, True, False],
        "task-b": [True, True, True],
        "task-c": [True, False, False],
    }
    assert pass_power(trials, 1) == 2 / 3
    assert pass_power(trials, 2) == 4 / 9                      # n>k：1/3、1、0 的平均
    assert pass_power({"all": [True, True], "not-all": [True, False]}, 2) == 1 / 2  # n=k 退化
    assert pass_power({}, 0) == 1.0                                # 边界
    try:
        pass_power({"short": [True]}, 2)
    except ValueError:
        pass
    else:
        raise AssertionError("insufficient trials must fail")


if __name__ == "__main__":
    self_test()
    print("160 ok: hands-on: add a trajectory diagnostic that does not affect final score")
