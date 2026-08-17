"""第06晚：CYK 成员判定与解析树回溯。"""

def cyk(word, terminal_rules, binary_rules, start):
    n = len(word)
    if n == 0:
        return False, None, {}
    table = [[set() for _ in range(n + 1)] for _ in range(n)]
    back = {}
    for i, ch in enumerate(word):
        for lhs in terminal_rules.get(ch, ()):
            table[i][i+1].add(lhs)
            back[(i, i+1, lhs)] = ch
    for length in range(2, n + 1):
        for i in range(n - length + 1):
            j = i + length
            for k in range(i + 1, j):
                for b in table[i][k]:
                    for c in table[k][j]:
                        for a in binary_rules.get((b,c), ()):
                            if a not in table[i][j]:
                                table[i][j].add(a)
                                back[(i,j,a)] = (k,b,c)
    def build(i, j, a):
        item = back[(i,j,a)]
        if isinstance(item, str):
            return (a, item)
        k,b,c = item
        return (a, build(i,k,b), build(k,j,c))
    ok = start in table[0][n]
    return ok, build(0,n,start) if ok else None, table

if __name__ == "__main__":
    # CNF：S->AB | AC, C->SB, A->a, B->b，生成 a^n b^n (n>=1)
    terminals = {"a":{"A"}, "b":{"B"}}
    binaries = {("A","B"):{"S"}, ("A","C"):{"S"}, ("S","B"):{"C"}}
    for word, expected in [("ab",True), ("aabb",True), ("aaabbb",True),
                           ("aab",False), ("abab",False), ("",False)]:
        ok, tree, _ = cyk(word, terminals, binaries, "S")
        print(word or "empty", ok, tree)
        assert ok == expected
    # 动手改造：让 back 保存所有候选，统计歧义文法的解析树数量。
