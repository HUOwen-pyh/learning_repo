"""第03晚：带 ε 边 NFA 与按需子集构造。"""
from collections import deque

EPS = None

class NFA:
    def __init__(self, states, alphabet, trans, start, accept):
        self.states, self.alphabet, self.trans = set(states), set(alphabet), trans
        self.start, self.accept = start, set(accept)

    def closure(self, states):
        out, stack = set(states), list(states)
        while stack:
            q = stack.pop()
            for nxt in self.trans.get((q, EPS), set()):
                if nxt not in out:
                    out.add(nxt)
                    stack.append(nxt)
        return frozenset(out)

    def step(self, states, ch):
        moved = set()
        for q in states:
            moved |= self.trans.get((q, ch), set())
        return self.closure(moved)

    def run(self, word):
        current = self.closure({self.start})
        trace = [current]
        for ch in word:
            current = self.step(current, ch)
            trace.append(current)
        return bool(current & self.accept), trace

def determinize(nfa):
    start = nfa.closure({nfa.start})
    todo, seen, delta = deque([start]), {start}, {}
    while todo:
        subset = todo.popleft()
        for ch in sorted(nfa.alphabet):
            nxt = nfa.step(subset, ch)
            delta[(subset, ch)] = nxt
            if nxt not in seen:
                seen.add(nxt); todo.append(nxt)
    accepts = {s for s in seen if s & nfa.accept}
    return start, seen, delta, accepts

def dfa_run(start, delta, accepts, word):
    q = start
    for ch in word:
        q = delta[(q, ch)]
    return q in accepts

if __name__ == "__main__":
    # 语言：包含 01 或包含 10。起点用 ε 同时分支。
    trans = {
        ("s", EPS): {"a0", "b0"},
        ("a0","0"): {"a0","a1"}, ("a0","1"): {"a0"}, ("a1","1"): {"ok"},
        ("b0","1"): {"b0","b1"}, ("b0","0"): {"b0"}, ("b1","0"): {"ok"},
        ("ok","0"): {"ok"}, ("ok","1"): {"ok"},
    }
    nfa = NFA({"s","a0","a1","b0","b1","ok"}, {"0","1"}, trans, "s", {"ok"})
    start, subsets, delta, accepts = determinize(nfa)
    for n in range(6):
        for i in range(1 << n):
            word = format(i, f"0{n}b") if n else ""
            expected, _ = nfa.run(word)
            assert dfa_run(start, delta, accepts, word) == expected
    print(f"NFA states={len(nfa.states)}, reachable DFA subsets={len(subsets)}")
    print("trace(0010):", nfa.run("0010")[1])
    # 动手改造：增加第三个 ε 分支识别以 11 结尾，并重新对拍。

