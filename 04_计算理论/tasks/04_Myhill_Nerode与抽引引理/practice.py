"""第04晚：表填充 DFA 最小化，并给出区分后缀。"""
from collections import deque

def reachable(states, alphabet, delta, start):
    seen, queue = {start}, deque([start])
    while queue:
        q = queue.popleft()
        for a in alphabet:
            nxt = delta[(q, a)]
            if nxt not in seen:
                seen.add(nxt); queue.append(nxt)
    return seen

def distinguishers(states, alphabet, delta, accept):
    """返回 unordered state-pair -> 一个区分后缀。"""
    pair = lambda x, y: tuple(sorted((x, y)))
    witness = {}
    for p in states:
        for q in states:
            if p < q and ((p in accept) != (q in accept)):
                witness[pair(p,q)] = ""
    changed = True
    while changed:
        changed = False
        for p in states:
            for q in states:
                key = pair(p,q)
                if p >= q or key in witness:
                    continue
                for a in alphabet:
                    next_key = pair(delta[(p,a)], delta[(q,a)])
                    if next_key in witness:
                        witness[key] = a + witness[next_key]
                        changed = True
                        break
    return witness

def equivalence_classes(states, witness):
    classes = []
    for q in sorted(states):
        for block in classes:
            if tuple(sorted((q, block[0]))) not in witness:
                block.append(q); break
        else:
            classes.append([q])
    return classes

if __name__ == "__main__":
    states = {"A","B","C","D","U"}  # U 不可达；B/D 行为等价
    alphabet = {"0","1"}
    delta = {
        ("A","0"):"A", ("A","1"):"B",
        ("B","0"):"C", ("B","1"):"B",
        ("C","0"):"B", ("C","1"):"D",
        ("D","0"):"C", ("D","1"):"D",
        ("U","0"):"U", ("U","1"):"U",
    }
    accept = {"B","D"}
    live = reachable(states, alphabet, delta, "A")
    witnesses = distinguishers(live, alphabet, delta, accept)
    blocks = equivalence_classes(live, witnesses)
    print("reachable:", sorted(live))
    print("equivalence classes:", blocks)
    print("distinguishing suffix A/B:", repr(witnesses[("A","B")]))
    assert "U" not in live
    assert any(set(b) == {"B","D"} for b in blocks)
    assert len(blocks) == 3
    # 动手改造：打印每个可区分状态对及其最短（或任一）区分后缀。
