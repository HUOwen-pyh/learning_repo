"""第08晚：有界模拟必须保留 UNKNOWN。"""
from dataclasses import dataclass

@dataclass(frozen=True)
class TinyProgram:
    start: int
    # state -> next state；None 表示停机
    next_state: dict

def bounded_halting(program: TinyProgram, budget: int):
    state = program.start
    seen = set()
    for step in range(budget + 1):
        if state is None:
            return "HALTS", step
        if state in seen:
            # 只因本教学模型是有限确定状态，重复配置才能证明 LOOP。
            return "LOOPS", step
        seen.add(state)
        state = program.next_state.get(state)
    return "UNKNOWN", budget

if __name__ == "__main__":
    stops = TinyProgram(0, {0:1, 1:None})
    loops = TinyProgram(0, {0:1, 1:0})
    slow = TinyProgram(0, {i:i+1 for i in range(50)} | {50:None})
    assert bounded_halting(stops, 10)[0] == "HALTS"
    assert bounded_halting(loops, 10)[0] == "LOOPS"
    print("slow with budget 10:", bounded_halting(slow, 10))
    print("slow with budget 60:", bounded_halting(slow, 60))
    assert bounded_halting(slow, 10)[0] == "UNKNOWN"
    assert bounded_halting(slow, 60)[0] == "HALTS"
    print("Conclusion: TIMEOUT/UNKNOWN is not evidence of non-halting.")
    # 动手改造：删掉 seen 优化，观察 LOOP 只能变成 UNKNOWN；解释一般程序为何更难。
