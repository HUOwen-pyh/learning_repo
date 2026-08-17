"""区分 context requirements、providers 与实际 effect trace。"""
from __future__ import annotations

import sys
from collections.abc import Callable
from dataclasses import dataclass

sys.stdout.reconfigure(encoding="utf-8")


@dataclass(frozen=True)
class Plugin:
    name: str
    requires: frozenset[str]
    provides: frozenset[str]
    declared_effects: frozenset[str]


def activate(plugins: list[Plugin], base: set[str]) -> tuple[list[str], set[str]]:
    available = set(base)
    pending = list(plugins)
    order: list[str] = []
    while pending:
        ready = next((plugin for plugin in pending if plugin.requires <= available), None)
        if ready is None:
            raise ValueError("missing or cyclic requirements")
        pending.remove(ready)
        available |= ready.provides
        order.append(ready.name)
    return order, available


def execute(plugin: Plugin, action: Callable[[Callable[[str], None]], None]) -> tuple[str, ...]:
    trace: list[str] = []
    action(trace.append)
    actual_effects = set(trace)
    undeclared = actual_effects - plugin.declared_effects
    if undeclared:
        raise PermissionError(f"undeclared effects: {sorted(undeclared)}")
    return tuple(trace)


def main() -> None:
    auth = Plugin("auth", frozenset(), frozenset({"credentials"}), frozenset())
    net = Plugin(
        "net",
        frozenset({"credentials"}),
        frozenset({"http"}),
        frozenset({"network", "audit"}),
    )
    assert activate([auth, net], set())[0] == ["auth", "net"]

    try:
        activate([Plugin("bad", frozenset({"ghost"}), frozenset(), frozenset())], set())
    except ValueError:
        pass
    else:
        raise AssertionError("缺失 coeffect/context requirement 应拒绝激活")

    assert execute(net, lambda emit: (emit("network"), emit("audit"))) == (
        "network",
        "audit",
    )  # actual == declared
    assert execute(net, lambda emit: emit("network")) == ("network",)  # 真子集允许
    try:
        execute(net, lambda emit: (emit("network"), emit("filesystem")))
    except PermissionError as error:
        assert "filesystem" in str(error)
    else:
        raise AssertionError("actual trace 超出 declared_effects 必须拒绝")
    print("context requirements 与 actual_trace⊆declared_effects 边界通过")


if __name__ == "__main__":
    main()

# 动手改造：让 trace 记录参数，并把 effect 名称检查与参数策略检查分层。
