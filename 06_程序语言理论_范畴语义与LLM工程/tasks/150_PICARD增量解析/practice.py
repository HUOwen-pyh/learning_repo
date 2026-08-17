"""括号语言的 PICARD 式 token 过滤。"""


def prefix_valid(text: str, pairs: dict[str, str]) -> bool:
    closers = {v: k for k, v in pairs.items()}
    stack: list[str] = []
    for char in text:
        if char in pairs:
            stack.append(char)
        elif char in closers:
            if not stack or stack.pop() != closers[char]:
                return False
        else:
            return False
    return True


def complete(text: str, pairs: dict[str, str]) -> bool:
    return prefix_valid(text, pairs) and sum(c in pairs for c in text) == sum(c in pairs.values() for c in text)


def allowed(prefix: str, tokens: tuple[str, ...], pairs: dict[str, str]) -> list[str]:
    return [token for token in tokens if prefix_valid(prefix + token, pairs)]


def self_test() -> None:
    pairs = {"(": ")"}
    assert allowed("(", ("(", ")", "))"), pairs) == ["(", ")"]  # 正例
    assert allowed("", (")",), pairs) == []                         # 反例
    assert prefix_valid("((", pairs) and not complete("((", pairs) # 边界


if __name__ == "__main__":
    self_test()
    print("150 ok: hands-on: add '[':']' and a mismatched-nesting assertion")
