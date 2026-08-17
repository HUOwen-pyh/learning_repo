"""持久栈与按配置缓存的演示。"""
from dataclasses import dataclass


@dataclass(frozen=True)
class Stack:
    head: str
    tail: "Stack | None" = None


def push(stack: Stack | None, value: str) -> Stack:
    return Stack(value, stack)


def pop(stack: Stack | None) -> tuple[str, Stack | None]:
    if stack is None:
        raise IndexError("empty persistent stack")
    return stack.head, stack.tail


def self_test() -> None:
    root = push(None, "root")
    left, right = push(root, "L"), push(root, "R")
    assert left.tail is root and right.tail is root            # 正例：共享
    assert pop(left) == ("L", root) and root.head == "root"  # 不可变
    try:
        pop(None)
    except IndexError:
        pass
    else:
        raise AssertionError("negative case must fail")
    assert push(None, "").head == ""                          # 边界


if __name__ == "__main__":
    self_test()
    print("152 ok: hands-on: add an intern table so identical nodes share identity")
