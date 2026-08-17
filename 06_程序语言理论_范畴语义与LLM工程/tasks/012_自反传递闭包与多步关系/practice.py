"""第012晚：一步图关系的自反传递闭包与路径证书。"""
from collections import deque
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

EDGES = {(0, 1), (1, 2), (1, 3), (3, 4)}

def verify_path(path: tuple[int, ...]) -> bool:
    return bool(path) and all((a, b) in EDGES for a, b in zip(path, path[1:]))

def find_path(start: int, goal: int) -> tuple[int, ...] | None:
    queue = deque([(start, (start,))])
    seen = {start}
    while queue:
        node, path = queue.popleft()
        if node == goal: return path
        for a, b in sorted(EDGES):
            if a == node and b not in seen:
                seen.add(b); queue.append((b, path + (b,)))
    return None

def main() -> None:
    assert verify_path((2,))                              # 最小正例：零步
    path = find_path(0, 4)
    assert path == (0, 1, 3, 4) and verify_path(path)
    assert not verify_path(())                            # 空元组不是带端点的证书
    assert not verify_path((0, 4))                        # 最小反例：非法跳边
    assert find_path(4, 0) is None
    print("通过：多步证书逐边核验，零步路径仍含一个端点。")

if __name__ == "__main__": main()

# 动手改造：实现两条首尾相接路径的组合，并拒绝端点不匹配。
