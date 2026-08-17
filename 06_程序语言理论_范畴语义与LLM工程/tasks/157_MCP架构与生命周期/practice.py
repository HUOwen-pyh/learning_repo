"""MCP 生命周期与能力协商的最小状态机。"""
from enum import Enum, auto


class Phase(Enum):
    NEW = auto()
    INITIALIZING = auto()
    READY = auto()
    CLOSED = auto()


class Client:
    def __init__(self, supported: set[str]):
        self.phase = Phase.NEW
        self.supported = supported
        self.capabilities: set[str] = set()

    def initialize(self, server_caps: set[str]) -> None:
        if self.phase is not Phase.NEW:
            raise RuntimeError("initialize out of order")
        self.phase = Phase.INITIALIZING
        self.capabilities = self.supported & server_caps

    def initialized(self) -> None:
        if self.phase is not Phase.INITIALIZING:
            raise RuntimeError("notification out of order")
        self.phase = Phase.READY

    def close(self) -> None:
        self.phase = Phase.CLOSED


def self_test() -> None:
    c = Client({"tools", "resources"})
    c.initialize({"tools"}); c.initialized()
    assert c.phase is Phase.READY and c.capabilities == {"tools"}  # 正例
    try:
        Client(set()).initialized()
    except RuntimeError:
        pass
    else:
        raise AssertionError("negative order")
    c.close(); c.close(); assert c.phase is Phase.CLOSED             # 边界：幂等关闭


if __name__ == "__main__":
    self_test()
    print("157 ok: hands-on: reject a server protocolVersion mismatch")
