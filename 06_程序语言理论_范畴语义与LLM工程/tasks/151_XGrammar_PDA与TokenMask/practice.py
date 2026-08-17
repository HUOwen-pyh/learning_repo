"""平衡括号 PDA 的词表 mask。"""


def consume(depth: int, token: str, max_depth: int) -> int | None:
    for char in token:
        if char == "(":
            depth += 1
            if depth > max_depth:
                return None
        elif char == ")":
            depth -= 1
            if depth < 0:
                return None
        else:
            return None
    return depth


def token_mask(depth: int, vocab: tuple[str, ...], max_depth: int) -> dict[str, bool]:
    return {token: consume(depth, token, max_depth) is not None for token in vocab}


def self_test() -> None:
    vocab = ("(", ")", "()", "((", "x")
    assert token_mask(0, vocab, 2) == {"(": True, ")": False, "()": True, "((": True, "x": False}
    assert consume(2, "(", 2) is None                       # 反例
    assert consume(0, "", 2) == 0                          # 边界


if __name__ == "__main__":
    self_test()
    print("151 ok: hands-on: add an EOS token allowed only at depth zero")
