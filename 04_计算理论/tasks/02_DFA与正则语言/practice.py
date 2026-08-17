"""第02晚：DFA、乘积与最短区分串。"""
from collections import deque
from dataclasses import dataclass

@dataclass(frozen=True)
class DFA:
    states: frozenset
    alphabet: frozenset
    transition: dict
    start: str
    accept: frozenset

    def run(self, word: str) -> tuple[bool, list[str]]:
        q, trace = self.start, [self.start]
        for ch in word:
            if ch not in self.alphabet:
                raise ValueError(f"symbol {ch!r} outside alphabet")
            q = self.transition[(q, ch)]
            trace.append(q)
        return q in self.accept, trace

def distinguishing_word(a: DFA, b: DFA):
    """返回最短区分串；None 表示等价。要求完整 DFA、相同字母表。"""
    assert a.alphabet == b.alphabet
    start = (a.start, b.start)
    queue = deque([(start, "")])
    seen = {start}
    while queue:
        (qa, qb), word = queue.popleft()
        if (qa in a.accept) != (qb in b.accept):
            return word
        for ch in sorted(a.alphabet):
            pair = (a.transition[(qa, ch)], b.transition[(qb, ch)])
            if pair not in seen:
                seen.add(pair)
                queue.append((pair, word + ch))
    return None

def parity_ones() -> DFA:
    tr = {(q, ch): (q if ch == "0" else ("odd" if q == "even" else "even"))
          for q in ("even", "odd") for ch in "01"}
    return DFA(frozenset(tr_q for tr_q, _ in tr), frozenset("01"), tr, "even", frozenset({"odd"}))

if __name__ == "__main__":
    odd = parity_ones()
    for w in ["", "0", "1", "1011"]:
        accepted, trace = odd.run(w)
        print(f"{w!r:6} accepted={accepted}, trace={trace}")
        assert accepted == (w.count("1") % 2 == 1)
    renamed = DFA(frozenset({"E", "O"}), frozenset("01"),
                  {("E", "0"):"E", ("E", "1"):"O", ("O", "0"):"O", ("O", "1"):"E"},
                  "E", frozenset({"O"}))
    assert distinguishing_word(odd, renamed) is None
    reject_all = DFA(frozenset({"r"}), frozenset("01"),
                     {("r","0"):"r", ("r","1"):"r"}, "r", frozenset())
    witness = distinguishing_word(odd, reject_all)
    print("shortest counterexample:", repr(witness))
    assert witness == "1"
    # 动手改造：实现 DFA 的交集构造，并验证 L∩补L 为空。
