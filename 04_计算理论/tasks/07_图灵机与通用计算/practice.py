"""第07晚：稀疏纸带图灵机模拟器。"""
from dataclasses import dataclass

@dataclass
class Result:
    status: str
    tape: str
    steps: int
    trace: list

def run_tm(transitions, start, halts, text, blank="_", limit=100):
    tape = {i: ch for i, ch in enumerate(text) if ch != blank}
    q, head, trace = start, 0, []
    for step in range(limit + 1):
        snapshot = (q, head, "".join(tape.get(i, blank) for i in range(-1, max(len(text)+2, head+2))))
        trace.append(snapshot)
        if q in halts:
            lo = min(tape, default=0); hi = max(tape, default=-1)
            return Result(q, "".join(tape.get(i, blank) for i in range(lo, hi+1)), step, trace)
        if step == limit:
            return Result("TIMEOUT", "", step, trace)
        symbol = tape.get(head, blank)
        if (q, symbol) not in transitions:
            return Result("STUCK", "", step, trace)
        q, write, move = transitions[(q, symbol)]
        if write == blank:
            tape.pop(head, None)
        else:
            tape[head] = write
        head += {"L":-1, "R":1, "S":0}[move]
    raise AssertionError("unreachable")

if __name__ == "__main__":
    unary_plus_one = {
        ("scan","1"):("scan","1","R"),
        ("scan","_"):("ACCEPT","1","S"),
    }
    result = run_tm(unary_plus_one, "scan", {"ACCEPT","REJECT"}, "111")
    print("status/tape/steps:", result.status, result.tape, result.steps)
    print("configuration trace:", result.trace)
    assert (result.status, result.tape) == ("ACCEPT", "1111")
    assert run_tm(unary_plus_one, "scan", {"ACCEPT"}, "", limit=5).tape == "1"
    # 动手改造：写一台判定一元长度为偶数的机器，明确 ACCEPT 与 REJECT。

