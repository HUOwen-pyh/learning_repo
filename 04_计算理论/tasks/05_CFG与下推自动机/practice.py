"""第05晚：歧义文法的解析计数与一个栈识别器。"""
from functools import lru_cache

@lru_cache(None)
def ambiguous_parses(expr: str):
    """文法 E -> E+E | a 的所有括号化解析。"""
    if expr == "a":
        return ("a",)
    trees = []
    for i, ch in enumerate(expr):
        if ch == "+":
            for left in ambiguous_parses(expr[:i]):
                for right in ambiguous_parses(expr[i+1:]):
                    trees.append(f"({left}+{right})")
    return tuple(trees)

def balanced_parentheses(word: str) -> bool:
    stack = []
    for ch in word:
        if ch == "(":
            stack.append(ch)
        elif ch == ")" and stack:
            stack.pop()
        else:
            return False
    return not stack

def left_associative(expr: str) -> str:
    atoms = expr.split("+")
    tree = atoms[0]
    for atom in atoms[1:]:
        tree = f"({tree}+{atom})"
    return tree

if __name__ == "__main__":
    trees = ambiguous_parses("a+a+a")
    print("ambiguous parse trees:", trees)
    assert len(trees) == 2
    assert left_associative("a+a+a") == "((a+a)+a)"
    cases = {"":True, "()":True, "(())":True, "()()":True, "(()":False, "())(":False}
    for word, expected in cases.items():
        assert balanced_parentheses(word) == expected
    print("PDA-style stack checks:", cases)
    # 动手改造：为 + 和 * 写分层文法对应的递归下降解析器，令 * 优先。

